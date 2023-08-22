import abc
import json


class DataLogger(abc.ABC):
    @abc.abstractmethod
    def log(self, system_prompt: str, prompts: [str], messages: [dict], model_name: str, temperature: float, top_p: float, n: int, stream: bool, presence_penalty: float, frequency_penalty: float, max_tokens: int, stop_sequences: [str], logit_bias: [float], response_id: str, response_created_at: str, response_model: str, response_choices: [str], usage_prompt_tokens: int, usage_completion_tokens: int, usage_total_tokens: int):
        pass


class LoggerSqlite3(DataLogger):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_tables(self):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
CREATE TABLE IF NOT EXISTS chaincrafter_log (
id INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
-- Chain and prompts data
system_prompt TEXT,
prompts BLOB,
-- Request data
messages BLOB,
model_name TEXT,
temperature REAL,
top_p REAL,
n INTEGER,
stream BOOLEAN,
presence_penalty REAL,
frequency_penalty REAL,
max_tokens INTEGER,
stop_sequences BLOB,
logit_bias BLOB,
-- Response data
response_id TEXT,
response_created_at DATETIME,
response_model TEXT,
response_choices BLOB,
usage_prompt_tokens INTEGER,
usage_completion_tokens INTEGER,
usage_total_tokens INTEGER
)""")
        conn.commit()

    def log(self, system_prompt: str, prompts: [str], messages: [dict], model_name: str, temperature: float, top_p: float, n: int, stream: bool, presence_penalty: float, frequency_penalty: float, max_tokens: int, stop_sequences: [str], logit_bias: [float], response_id: str, response_created_at: str, response_model: str, response_choices: [str], usage_prompt_tokens: int, usage_completion_tokens: int, usage_total_tokens: int):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        values = {
            "system_prompt": system_prompt,
            "prompts": json.dumps(prompts),

            "messages": json.dumps(messages),
            "model_name": model_name,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "max_tokens": max_tokens,
            "stop_sequences": json.dumps(stop_sequences),
            "logit_bias": json.dumps(logit_bias),

            "response_id": response_id,
            "response_created_at": response_created_at,
            "response_model": response_model,
            "response_choices": json.dumps(response_choices),
            "usage_prompt_tokens": usage_prompt_tokens,
            "usage_completion_tokens": usage_completion_tokens,
            "usage_total_tokens": usage_total_tokens,
        }
        columns = ",".join(values.keys())
        keys = ",".join([':' + key for key in values.keys()])
        c.execute(f"INSERT INTO chaincrafter_log ({columns}) VALUES ({keys})", values)
        conn.commit()
