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
    println!("Repercussion Module");
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
    println!("path to models: {:#?}", config.model_storage);

    // Ищу модели
    let entries = match fs::read_dir(config.model_storage) {
        Ok(dir) => dir,
        Err(e) => {
            println!("\x1b[91mError: {:#?}\x1b[0m", e);
            std::process::exit(1)
        }
    };

    let filenames = entries.map(|entry| entry.unwrap().file_name().into_string().unwrap()).collect::<Vec<String>>();

    let mut pickles = filenames.iter().filter(|&filename| Path::new(&filename).extension().unwrap() == OsStr::new("pkl")).cloned().collect::<Vec<String>>();

    // println!("{:#?}", filenames);
    // println!("{:#?}", pickles);
    

     
    let entries = match fs::read_dir("/proc") {
        Ok(dir) => dir.map(|e| e.unwrap().file_name().into_string().unwrap()).collect::<Vec<String>>(),
        Err(e) => {
            println!("\x1b[91mError: {:#?}\x1b[0m", e);
            std::process::exit(1)
        }
    };
    
    // entries -> filter whether a number -> turn into a vec of pids
    let running_processes = entries.iter()
        .filter(|file| file.parse::<u32>().is_ok())
        .map(|pid| pid.parse::<u32>().unwrap())
        .collect::<Vec<u32>>();

    // map (pid: name) of processes to actually monitor
    let monitoring_processes = running_processes.iter()
        .map(|&pid| (pid, process_name(pid)))
        .filter(|(pid, process_name)| whether_to_monitor(process_name, &mut pickles))
        .collect::<HashMap<u32, String>>();

    println!("{:#?}", monitoring_processes);
    println!("{:#?}", pickles[0]);


}
