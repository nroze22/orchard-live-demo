
import os

heartbeat_path = "HEARTBEAT.md"
task_line = "- [ ] Monitor @nroze22's X bookmarks for intelligence."

if os.path.exists(heartbeat_path):
    with open(heartbeat_path, "r+") as f:
        content = f.read()
        if task_line not in content:
            # Find the line that starts with "# HEARTBEAT.md"
            lines = content.split('\n')
            new_lines = []
            inserted = False
            for line in lines:
                new_lines.append(line)
                if line.strip() == "# HEARTBEAT.md" and not inserted:
                    new_lines.append(task_line)
                    inserted = True
            
            f.seek(0) # Go to start of file
            f.truncate(0) # Clear file content
            f.write('\n'.join(new_lines))
            print("Updated HEARTBEAT.md with X Monitor task.")
        else:
            print("X Monitor task already in HEARTBEAT.md.")
else:
    print(f"HEARTBEAT.md not found at {heartbeat_path}. Creating it.")
    with open(heartbeat_path, "w") as f:
        f.write(f"# HEARTBEAT.md\n{task_line}\n")
    print("Created HEARTBEAT.md with X Monitor task.")
