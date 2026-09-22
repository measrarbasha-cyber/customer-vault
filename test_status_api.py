import urllib.request
import json

# 1. Test Stats endpoint
req = urllib.request.urlopen('http://localhost:5000/api/customers/stats')
stats = json.loads(req.read().decode('utf-8'))
print('Stats endpoint response:', stats)

# 2. Test status filtering for Pending
req = urllib.request.urlopen('http://localhost:5000/api/customers?status=Pending')
pending = json.loads(req.read().decode('utf-8'))
print(f'Pending customers count: {len(pending)}')

# 3. Test quick status update (move customer 66 to Completed)
data = json.dumps({'status': 'Completed'}).encode('utf-8')
req = urllib.request.Request('http://localhost:5000/api/customers/66/status', data=data, headers={'Content-Type': 'application/json'}, method='POST')
resp = urllib.request.urlopen(req)
updated = json.loads(resp.read().decode('utf-8'))
print(f"Moved Customer 66 to: {updated.get('status')}")

# 4. Re-check stats endpoint
req = urllib.request.urlopen('http://localhost:5000/api/customers/stats')
new_stats = json.loads(req.read().decode('utf-8'))
print('New Stats response:', new_stats)

# 5. Move customer 66 back to Pending
data = json.dumps({'status': 'Pending'}).encode('utf-8')
req = urllib.request.Request('http://localhost:5000/api/customers/66/status', data=data, headers={'Content-Type': 'application/json'}, method='POST')
urllib.request.urlopen(req)
print('Reset Customer 66 back to Pending successfully!')
