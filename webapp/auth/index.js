import express from 'express';

const authRouter = express.Router();
const tempUserLoginInfo = {
  'jun_hong@gmail.com': '1234',
};
authRouter.post('/signin', (request, response) => {
  console.log(`request body at router: ${JSON.stringify(request.body)}`);
  const user_id_input = request.body.id;
  const user_pw_input = request.body.pw;

  if (
    user_id_input in tempUserLoginInfo &&
    tempUserLoginInfo[user_id_input] === user_pw_input
  ) {
    console.log('login success');
    return response.status(200).json({
      msg: 'login success',
    });
  } else {
    console.log('login failed');
    return response.status(404).json({
      msg: 'login failed',
    });
  }
});

export default authRouter;
