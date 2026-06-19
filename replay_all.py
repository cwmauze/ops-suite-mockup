import json
import os
import subprocess

log_file = '/Users/charlie/.gemini/antigravity-ide/brain/33a79cb7-9abc-443d-b35e-6e7b460dfcbd/.system_generated/logs/transcript.jsonl'

with open(log_file, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    name = call['name']
                    args = call.get('args', {})
                    
                    if name == 'run_command':
                        cmd = args.get('CommandLine', '')
                        if 'mv ' in cmd or 'cp ' in cmd:
                            if 'manifest.html' in cmd or 'home.html' in cmd or 'index.html' in cmd or 'flightlog.html' in cmd:
                                print(f"Running: {cmd}")
                                subprocess.run(cmd, shell=True, cwd='/Users/charlie/Desktop/Apps/Ops Suite/prototype')
                    
                    elif name == 'write_to_file':
                        target = args.get('TargetFile', '')
                        if target.endswith('.html'):
                            print(f"Write to: {target}")
                            with open(target, 'w') as out:
                                out.write(args.get('CodeContent', ''))
                                
                    elif name == 'replace_file_content':
                        target = args.get('TargetFile', '')
                        if target.endswith('.html'):
                            print(f"Replace in: {target}")
                            try:
                                with open(target, 'r') as file:
                                    content = file.read()
                                target_content = args.get('TargetContent', '')
                                replacement = args.get('ReplacementContent', '')
                                if target_content in content:
                                    content = content.replace(target_content, replacement)
                                    with open(target, 'w') as file:
                                        file.write(content)
                                else:
                                    print(f"  -> Target not found in {target}!")
                            except Exception as e:
                                print(f"Error: {e}")
                                
                    elif name == 'multi_replace_file_content':
                        target = args.get('TargetFile', '')
                        if target.endswith('.html'):
                            print(f"Multi-replace in: {target}")
                            try:
                                with open(target, 'r') as file:
                                    content = file.read()
                                chunks = args.get('ReplacementChunks', [])
                                for chunk in chunks:
                                    target_content = chunk.get('TargetContent', '')
                                    replacement = chunk.get('ReplacementContent', '')
                                    if target_content in content:
                                        content = content.replace(target_content, replacement)
                                    else:
                                        print(f"  -> Target chunk not found in {target}!")
                                with open(target, 'w') as file:
                                    file.write(content)
                            except Exception as e:
                                print(f"Error: {e}")

        except Exception as e:
            pass

print("Replay finished.")
