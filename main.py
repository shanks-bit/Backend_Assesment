from fastapi import FastAPI
from routes.entry import entry_root
from routes.user import user_root


app = FastAPI()

app.include_router(entry_root)
app.include_router(user_root)
