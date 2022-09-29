import os
import sys
import subprocess

MAPPINGS_DIR = 'mappings'
GRADLE_TASKS = ['clean', 'feather', 'build', 'javadoc', 'javadocJar', 'checkMappings', 'mapCalamusJar', 'mapNamedJar', 'publish', 'separateMappings', 'insertMappings', 'propagateMappingsDown', 'propagateMappingsUp', 'propagateMappings']
GRADLEW = 'gradlew' if os.name == 'nt' else './gradlew'

def main():
    possible_versions = find_minecraft_versions()
    versions = []
    tasks = []
    
    args = sys.argv
    
    for i in range(1, len(args)):
        arg = args[i]
        
        if arg in possible_versions:
            versions.append(arg)
        elif arg in GRADLE_TASKS:
            tasks.append(arg)
        else:
            raise Exception('unrecognized arg ' + arg + '!')
    
    if len(versions) == 0:
        if 'MC_VERSION' in os.environ:
            version = os.environ['MC_VERSION']
            
            if is_minecraft_version(version):
                versions.append(version)
            else:
                raise Exception('no minecraft version given!')
        else:
            versions = possible_versions
    if len(tasks) == 0:
        raise Exception('no gradle tasks given!')
    
    command = [GRADLEW]
    command.extend(tasks)
    command.append('--stacktrace')
    
    for version in versions:
        os.environ['MC_VERSION'] = version
        subprocess.run(" ".join(command), shell = True, check = True)

def find_minecraft_versions():
    versions = []
    
    for filename in os.listdir(MAPPINGS_DIR):
        path = os.path.join(MAPPINGS_DIR, filename)
        
        if filename.endswith('.tiny'):
            versions.append(filename[0:len(filename) - len('.tiny')])
        elif filename.endswith('.tinydiff'):
            raw_pair = filename[0:len(filename) - len('.tinydiff')]
            pair = raw_pair.split('#')
            
            if len(pair) == 2:
                versions.append(pair[-1])
    
    return versions

if __name__ == '__main__':
    main()
