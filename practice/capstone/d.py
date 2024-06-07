from configparser import ConfigParser


config = ConfigParser()
try:
    config.read("default.ini")
except:
    print("default.ini reading went wrong")
    raise SystemExit()

print(int(config["DEFAULT"]["files_count"]))
print(str(config["DEFAULT"]["file_name"]))
print(int(config["DEFAULT"]["data_lines"]))
print(str(config["DEFAULT"]["clear_path"]))
print(str(config["DEFAULT"]["file_prefix"]))
print(int(config["DEFAULT"]["multiprocessing"]))