import json
import os

log_file = '/Users/charlie/.gemini/antigravity-ide/brain/33a79cb7-9abc-443d-b35e-6e7b460dfcbd/.system_generated/logs/transcript.jsonl'

latest_content = None

with open(log_file, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            # check tool calls
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    if call['name'] == 'default_api:write_to_file':
                        args = call.get('args', {})
                        if 'flightlog.html' in args.get('TargetFile', ''):
                            latest_content = args.get('CodeContent')
        except:
            pass

if latest_content:
    print(f"Recovered flightlog.html (len {len(latest_content)}) from write_to_file")
    with open('/Users/charlie/Desktop/Apps/Ops Suite/prototype/flightlog.html', 'w') as f:
        f.write(latest_content)
else:
    print("Could not find full write_to_file for flightlog.html. Checking for other tools.")
