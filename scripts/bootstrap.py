import asyncio, json, os
from pathlib import Path
import httpx
BASE=os.getenv("TRESTLE_URL","http://127.0.0.1:7333").rstrip("/"); EMAIL=os.getenv("TRESTLE_ADMIN_EMAIL"); PASSWORD=os.getenv("TRESTLE_ADMIN_PASSWORD")
if not EMAIL or not PASSWORD: raise SystemExit("Set TRESTLE_ADMIN_EMAIL and TRESTLE_ADMIN_PASSWORD")
async def main():
 async with httpx.AsyncClient(base_url=BASE,timeout=15,trust_env=False) as c:
  status=(await c.get("/admin/v1/setup/status")).json(); endpoint="/admin/v1/setup" if status.get("setupRequired") else "/admin/v1/session"; login=await c.post(endpoint,json={"email":EMAIL,"password":PASSWORD,"applicationRegistrationPolicy":"closed"},headers={"origin":BASE}); login.raise_for_status(); csrf=login.json().get("csrfToken",""); headers={"origin":BASE,"x-trestle-csrf":csrf}; existing=(await c.get("/admin/v1/collections")).json()["items"]
  if "fn_observations" not in [x["name"] for x in existing]:
   schema={"name":"fn_observations","fields":[{"name":"title","type":"text","required":True},{"name":"location","type":"text","required":True},{"name":"category","type":"select","required":True,"default":"flora"},{"name":"condition","type":"select","required":True,"default":"stable"},{"name":"notes","type":"text"},{"name":"temperature","type":"number"}]}; r=await c.post("/admin/v1/collections",json=schema,headers=headers);r.raise_for_status()
  rules={"rules":{key:'actor.kind == "service"' for key in ("list","view","create","update","delete")}};r=await c.put("/admin/v1/collection-rules/fn_observations",json=rules,headers=headers);r.raise_for_status()
  target=Path(".field-notebook.json"); saved=json.loads(target.read_text()) if target.exists() else {}
  if not saved.get("serviceToken"):
   r=await c.post("/admin/v1/credentials",json={"kind":"service","name":"Field Notebook","scopes":["records:read","records:write"]},headers=headers);r.raise_for_status();saved["serviceToken"]=r.json()["secret"]
  saved["trestleURL"]=BASE;target.write_text(json.dumps(saved,indent=2)+"\n");target.chmod(0o600)
 print("Field Notebook is ready.")
asyncio.run(main())
