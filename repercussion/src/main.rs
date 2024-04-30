use color_eyre::{eyre::eyre, Report, Result};
use serde::Deserialize;
use std::{
    collections::HashMap,
    env,
    ffi::OsStr,
    fs,
    io::{BufRead, BufReader},
    path::{Path, PathBuf},
};
use toml;

use cgroups_rs::{cgroup_builder::*, *};
use pyo3::{
    prelude::*,
    types::{PyAny, PyList},
};

#[derive(Deserialize, Debug)]
struct Config {
    model_storage: PathBuf,
    debug: bool,
}

fn process_name(pid: u64) -> Result<String> {
    let file = fs::File::open(format!("/proc/{}/status", pid))?;
    let mut buffer = BufReader::new(file);
    let mut first_line = String::new();
    let _ = buffer.read_line(&mut first_line)?;
    let process_name = first_line
        .split_whitespace()
        .collect::<Vec<&str>>()
        .get(1)
        .ok_or(eyre!("No process name"))?
        .to_string();
    Ok(process_name)
}

fn process_to_monitor(pickle: &String) -> &str {
    return Path::new(pickle).file_stem().unwrap().to_str().unwrap();
}

fn whether_to_monitor(process: &String, pattern: &HashMap<usize, String>) -> bool {
    let result: Vec<String> = pattern
        .iter()
        .map(|(_, p)| p)
        .filter(|p| process.contains(process_to_monitor(p)))
        .cloned()
        .collect();
    return !result.is_empty();
}

fn why_monitor(process: String, pattern: &HashMap<usize, String>) -> usize {
    for (id, pickle) in pattern.into_iter() {
        if process.contains(process_to_monitor(&pickle)) {
            return *id;
        }
    }
    return 0;
}

fn which_to_monitor(pickles: &HashMap<usize, String>) -> Result<HashMap<u64, (String, usize)>> {
    let entries: Vec<String> = fs::read_dir("/proc")?
        .map(|e| {
            Ok(e?
                .file_name()
                .into_string()
                .map_err(|_| eyre!("Entries from /proc"))?)
        })
        .collect::<Result<_>>()?;

    // entries -> filter whether a number -> turn into a vec of pids
    let running_processes: Vec<u64> = entries
        .iter()
        .filter(|file| file.parse::<u64>().is_ok())
        .map(|pid| pid.parse::<u64>().unwrap())
        .collect();

    // map (pid: name) of processes to actually monitor
    let processes_to_monitor: HashMap<u64, (String, usize)> = running_processes
        .iter()
        .flat_map(|&pid| Ok::<_, Report>((pid, process_name(pid)?)))
        .filter(|(_pid, process_name)| whether_to_monitor(process_name, &pickles))
        .map(|(pid, process_name)| {
            (
                pid,
                (process_name.clone(), why_monitor(process_name, &pickles)),
            )
        })
        .collect();

    return Ok(processes_to_monitor);
}

fn import_model<'py>(path_to_model: &String, py: Python<'py>) -> PyResult<&'py PyAny> {
    let joblib = PyModule::import_bound(py, "joblib")?;
    let total: &PyAny = joblib.getattr("load")?.call1((path_to_model,))?.extract()?;
    Ok(total)
}

fn cgjail(pid: u64, process_name: String, id: usize, models: &HashMap<usize, &PyAny>) -> Result<()> {
    let jail_name = format!("{}_jail", process_name);

    let cpu_usage_quota = models[&id].getattr("cpu_usage_quota")?.extract::<i64>()?;
    let mem_max_bytes = models[&id].getattr("mem_max_bytes")?.extract::<i64>()?;
    let maximum_number_of_processes = models[&id]
        .getattr("maximum_number_of_processes")?
        .extract::<i64>()?;

    // get hierarchy (V2 or V1)
    let hier = cgroups_rs::hierarchies::auto();

    // creation of a cgroup wuth given limits
    let cgjail: Cgroup = CgroupBuilder::new(&jail_name)
        .memory()
        .memory_hard_limit(mem_max_bytes) // limit is i64, bytes
        .done()
        .cpu()
        .quota(cpu_usage_quota) // quota is i64
        .done()
        .pid()
        .maximum_number_of_processes(MaxValue::Value(maximum_number_of_processes)) // value is i64
        .done()
        .build(hier)?;

    let cpus: &cgroups_rs::cpu::CpuController = cgjail
        .controller_of()
        .ok_or(eyre!("Something went wrong in a CpuController"))?;
    cpus.add_task_by_tgid(&CgroupPid::from(pid))?;

    let memories: &cgroups_rs::memory::MemController = cgjail
        .controller_of()
        .ok_or(eyre!("Something went wrong in a MemController"))?;
    memories.add_task(&CgroupPid::from(pid))?;

    let pids: &cgroups_rs::pid::PidController = cgjail
        .controller_of()
        .ok_or(eyre!("Something went wrong in a PidController"))?;
    pids.add_task(&CgroupPid::from(pid))?;

    Ok(())
}

fn main() -> Result<()> {
    // the path to config_file is hardcoded
    let mut config_file_path = env::current_dir()?;
    config_file_path.pop();
    config_file_path.push("config/cgjailConfig.toml");

    let config_file = fs::read_to_string(config_file_path)?;

    let config: Config = toml::from_str(&config_file)?;

    // Pickles made by Reliability
    let entries = fs::read_dir(&config.model_storage)?;

    let filenames: Vec<String> = entries
        .map(|entry| {
            Ok(entry?
                .file_name()
                .into_string()
                .map_err(|_| eyre!("OS string conversion"))?)
        })
        .collect::<Result<_>>()?;

    let pickles: HashMap<usize, String> = filenames
        .into_iter()
        .filter(|filename| {
            Path::new(&filename)
                .extension()
                .is_some_and(|ext| ext == OsStr::new("pkl"))
        })
        .enumerate()
        .map(|(i, x)| (i + 1, x))
        .collect();

    let model_storage_as_string = config
        .model_storage
        .into_os_string()
        .into_string()
        .map_err(|_| eyre!("Model storage path buff to string conversion"))?;

    let models_to_load: HashMap<usize, String> = pickles
        .iter()
        .map(|(&id, pickle)| (id, format!("{}/{}", model_storage_as_string, pickle)))
        .collect();

    if config.debug {
        println!("All the pickeles:\n{:#?}", pickles);
    }

    let mut python_path = env::current_dir()?;
    python_path.push("predict.py");

    let py_app = fs::read_to_string(&python_path)?;

    Python::with_gil(|py| -> Result<()> {
        // import all the existing models once and for all
        let models: HashMap<usize, &PyAny> = models_to_load
            .into_iter()
            .map(|(id, model)| Ok((id, import_model(&model, py)?)))
            .collect::<PyResult<_>>()?;

        // unending loop - daemon behaviour
        loop {
            let processes_to_monitor = which_to_monitor(&pickles)?;

            let syspath = py
                .import_bound("sys")?
                .getattr("path")?
                .downcast_into::<PyList>()
                .map_err(|e| eyre!("{}", e))?;
            syspath.insert(0, &python_path.parent().map(|p| p.parent()))?;

            // loop through every process to monitor
            for (pid, (process_name, id)) in processes_to_monitor.into_iter() {
                
                if config.debug {
                    println!("Process {}: {} {}", pid, process_name, id);
                }

                let app: Py<PyAny> = PyModule::from_code_bound(py, &py_app, "", "")?
                    .getattr("predict")?
                    .into();
                let sentence: u32 = app.call1(py, (pid, models[&id]))?.extract::<u32>(py)?;

                if sentence == 1 {
                    println!("Process {} {} is naughty", pid, process_name);
                    cgjail(pid, process_name, id, &models)?;
                }
            }
            // for testing only run once
            if config.debug {
                break;
            }
        }

        Ok(())
    })?;

    Ok(())
}
