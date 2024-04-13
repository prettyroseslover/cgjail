#![allow(dead_code)]
#![allow(unused_variables)]

use std::ffi::OsStr;
use std::fs;
use std::path::{Path, PathBuf};
use serde::Deserialize;
use toml;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

#[derive(Deserialize, Debug)]
struct Config {
    model_storage: PathBuf
}

fn process_name(pid: u32) -> String{
    let file = match fs::File::open(format!("/proc/{}/status", pid)) {
        Ok(file) => file,
        Err(_) => {
            println!("\x1b[91mError: Unable to read a proc file\x1b[0m");
            std::process::exit(1)
        }
    };
    let mut buffer = BufReader::new(file);
    let mut first_line = String::new();
    let _ = buffer.read_line(&mut first_line);
    return first_line.split_whitespace().collect::<Vec<_>>()[1].to_string();
}

fn process_to_monitor(pickle: &String) -> &str{
    return Path::new(pickle).file_stem().unwrap().to_str().unwrap();
}

fn whether_to_monitor(process: &String, pattern: &mut Vec<String>) -> bool {
    let result: Vec<String> = pattern.iter().filter(|p| process.contains(process_to_monitor(p))).cloned().collect();
    return !result.is_empty()
}


fn main() {
    
    // the path to config_file is hardcoded
    let config_file_path = Path::new("/home/prettyroseslover/Sync/4th year/Laurea/cgjail/config/cgjailConfig.toml");

    let config_file = match fs::read_to_string(config_file_path) {
        Ok(s) => s,
        Err(e) => {
            println!("\x1b[91mError: {:#?}\x1b[0m", e);
            std::process::exit(1)
        }
    };

    let config: Config = toml::from_str(&config_file).unwrap();

    // Pickles made by Reliability
    let entries = match fs::read_dir(&config.model_storage) {
        Ok(dir) => dir,
        Err(e) => {
            println!("\x1b[91mError: {:#?}\x1b[0m", e);
            std::process::exit(1)
        }
    };

    let filenames: Vec<String> = entries.map(|entry| entry.unwrap().file_name().into_string().unwrap()).collect();

    let mut pickles:Vec<String> = filenames.iter().filter(|&filename| Path::new(&filename).extension().unwrap() == OsStr::new("pkl")).cloned().collect();

    let entries: Vec<String> = match fs::read_dir("/proc") {
        Ok(dir) => dir.map(|e| e.unwrap().file_name().into_string().unwrap()).collect(),
        Err(e) => {
            println!("\x1b[91mError: {:#?}\x1b[0m", e);
            std::process::exit(1)
        }
    };
    
    // entries -> filter whether a number -> turn into a vec of pids
    let running_processes: Vec<u32> = entries.iter()
        .filter(|file| file.parse::<u32>().is_ok())
        .map(|pid| pid.parse::<u32>().unwrap())
        .collect();

    // map (pid: name) of processes to actually monitor
    let monitoring_processes: HashMap<u32, String> = running_processes.iter()
        .map(|&pid| (pid, process_name(pid)))
        .filter(|(pid, process_name)| whether_to_monitor(process_name, &mut pickles))
        .collect();

    println!("{:#?}", monitoring_processes);
    println!("{:#?}", pickles[0]);


}
