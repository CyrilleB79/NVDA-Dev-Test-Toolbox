import re
import sys

def main():
    if len(sys.argv) < 2:
        print('Usage: extractChangeLog.py <refTag>')
        sys.exit(1)

    refTag = sys.argv[1]
    print(f'===> Ref tag:{refTag}')

    pattern = r'[Vv](-?\d+\.-?\d+.*?)(?:-dev-.*)?$'
    version = re.search(pattern, refTag).group(1)
    print(f'===> Version:{version}')

    pattern = rf'## Change log.*### Version {version}\s*(.*?)\s*(\n(### Version)|(\[\d+\]:)|$)'
    fileContent = open('readme.md', 'r', encoding='utf8').read()
    match = re.search(pattern, fileContent, re.DOTALL)
    changeLog = match.group(1) if match else ""
    changeLog += '\n'
    print(f'===> ChangeLog:\n<<<{changeLog}>>>\n')

    open('changelog.md', 'w', encoding='utf-8').write(changeLog)

if __name__ == '__main__':
    main()
