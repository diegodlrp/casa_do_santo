// server.js
import express from 'express';
import { handler } from './build/handler.js';

const app = express();
app.use(handler);

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`SvelteKit running on http://localhost:${port}`);
});
