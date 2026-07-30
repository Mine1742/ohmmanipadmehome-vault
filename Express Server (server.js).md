
Express is small, honest software—it does very little, and that’s why it’s powerful. Let’s build the mental model first, then look at real code without drowning in framework trivia.

I’ll assume **Node.js is installed** and we’re talking about a file called `server.js`.

---

## What Express _is_ (and is not)

Express is **an HTTP request router**.

That’s it.

It does **not**:

- manage threads
    
- scale your app
    
- store data
    
- secure anything by default
    

It **does**:

- listen for HTTP requests
    
- match URLs + methods
    
- run your code
    
- send HTTP responses
    

Think of Express as:

> “When a request looks like _this_, run _that_ function.”

---

## The smallest possible Express server

`// server.js const express = require('express'); const app = express();  app.listen(3000, () => {   console.log('Server running on http://localhost:3000'); });`

What just happened:

- `require('express')` loads the library
    
- `express()` creates an **app object**
    
- `app.listen` opens a TCP port and waits
    

Right now:

- the server runs
    
- it answers nothing
    
- every request gets a 404
    

---

## Requests and responses (the core loop)

Every Express handler looks like this:

`(req, res) => {   // read request   // write response }`

- `req` = incoming HTTP request
    
- `res` = outgoing HTTP response
    

That’s the whole contract.

---

## Your first route

`app.get('/', (req, res) => {   res.send('Hello world'); });`

This means:

- HTTP **GET**
    
- path `/`
    
- run this function
    
- send text back
    

Now when you hit:

`http://localhost:3000/`

You get:

`Hello world`

No magic. Just string in, string out.

---

## HTTP methods matter

These are different routes:

`app.get('/users', ...) app.post('/users', ...) app.put('/users', ...) app.delete('/users', ...)`

Same URL. Different **intent**.

Rough semantics:

- GET → read
    
- POST → create
    
- PUT → replace
    
- PATCH → update
    
- DELETE → remove
    

Express does not enforce meaning. Humans do.

---

## JSON APIs (this is what you’ll actually build)

First, enable JSON parsing:

`app.use(express.json());`

This tells Express:

> “If the request body is JSON, parse it.”

Now a POST endpoint:

`app.post('/devices', (req, res) => {   const device = req.body;    res.status(201).json({     message: 'Device created',     device   }); });`

If you send:

`{   "hostname": "LAP-123",   "owner": "alice" }`

Express:

- parses the JSON
    
- puts it on `req.body`
    
- you respond with structured data
    

---

## req: what you can read

Common request properties:

`req.method      // GET, POST, etc req.path        // /devices req.params      // URL parameters req.query       // ?page=2 req.headers     // HTTP headers req.body        // JSON body (if enabled)`

Example:

``app.get('/devices/:id', (req, res) => {   const id = req.params.id;   res.send(`Device ${id}`); });``

Request:

`/devices/42`

Response:

`Device 42`

---

## res: how you respond

Common response methods:

`res.send()      // text or auto JSON res.json()      // JSON res.status()    // set HTTP status res.sendStatus()// status + text`

Typical API response:

`res.status(404).json({ error: 'Not found' });`

Status codes matter. Clients rely on them.

---

## Middleware (Express’s secret weapon)

Middleware = functions that run **before** your route.

`app.use((req, res, next) => {   console.log(req.method, req.path);   next(); });`

Key rule:

- call `next()` → continue
    
- don’t → request stops
    

Middleware is used for:

- logging
    
- auth
    
- validation
    
- parsing
    
- rate limiting
    

Order matters. Express runs top → bottom.

---

## Example: simple auth middleware

`function requireApiKey(req, res, next) {   if (req.headers['x-api-key'] !== 'secret') {     return res.status(401).json({ error: 'Unauthorized' });   }   next(); }  app.get('/secure', requireApiKey, (req, res) => {   res.send('You made it'); });`

This pattern scales all the way to OAuth.

---

## Error handling (special middleware)

Errors bubble differently:

`app.use((err, req, res, next) => {   console.error(err);   res.status(500).json({ error: 'Server error' }); });`

If you call:

`next(new Error('Boom'));`

Express jumps to this handler.

---

## Typical Express project shape

`server.js routes/   devices.js controllers/ services/`

Express doesn’t force structure. Teams do.

---

## How Express fits into modern Azure stacks

You will see Express used as:

- API backend behind Azure App Service
    
- Container App
    
- API behind Azure APIM
    
- Dev tool / internal service
    

Authentication usually comes from:

- Azure AD OIDC middleware
    
- API gateways
    
- Managed Identity upstream
    

Express itself stays dumb. That’s a feature.

---

## Mental model to keep forever

> Express is a conveyor belt:  
> Request → middleware → route → response

Everything you learn builds on that.