import express from 'express';
import dotenv from 'dotenv';
import authRouter from './auth/index.js';
import cors from 'cors';
import multer from 'multer';
const upload = multer();

dotenv.config();
const PORT = parseInt(process.env.PORT, 10);
const corsOption = {
  origin: (origin, callback) => {
    if (!origin) {
      return callback(null, true);
    }

    // const host = origin.split('://')[1]
    // const allowedHost = ['localhost:3000']
    // const allowed = allowedHost.includes(host)
    callback(null, true);
  },
  credentials: true,
};

export default class Server {
  constructor() {
    this.app = express();
    this.setup();
  }

  setup = () => {
    this.app.use(cors(corsOption));
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
    this.app.use(upload.array());
    this.app.use(express.static('public'));
    this.app.get('/health', (request, response) => {
      return response.status(200).send('server healthy');
    });
    this.app.use('/auth', authRouter);
  };

  start = () => {
    this.app.listen(PORT || 3000, () => {
      console.log(`Server Listening on port ${PORT}`);
    });
    return;
  };
}
