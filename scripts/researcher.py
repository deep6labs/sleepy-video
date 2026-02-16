import yaml
import json
import subprocess
import os

def generate_facts(topic, count):
    prompt = f"Generate exactly {count} interesting and verifiable facts about {topic}. Output ONLY a JSON list of strings."
    
    # Switch to cloud model to avoid local CUDA OOM
    cmd = ["ollama", "run", "gemini-3-flash-preview:cloud", prompt]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error calling Ollama: {result.stderr}")
        return []
    
    try:
        # Clean up output to find JSON
        output = result.stdout.strip()
        start = output.find("[")
        end = output.rfind("]") + 1
        facts = json.loads(output[start:end])
        return facts
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return []

def main():
    config_path = "/home/asha/repos/sleepy-video/biz/sleepy-video-input-template.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    topic = config.get('topic_phrase', 'Stoic Wisdom')
    count = 10 # Hardcoded for fast recovery build
    
    print(f"Generating {count} facts for: {topic}...")
    facts = generate_facts(topic, count)
    
    output_path = "/home/asha/repos/sleepy-video/data/research_facts.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(facts, f, indent=2)
    
    print(f"Successfully saved {len(facts)} facts to {output_path}")

if __name__ == "__main__":
    main()
