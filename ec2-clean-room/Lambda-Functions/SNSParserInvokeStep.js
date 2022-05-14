const aws = require("aws-sdk");

exports.handler = (event, context, callback) => {
  console.log(JSON.stringify(event))
  console.log(event.Records[0].Sns.Message)
  var stepfunctions = new aws.StepFunctions();
  var stepMessage = JSON.parse(event.Records[0].Sns.Message);
  console.log(stepMessage.detail);
  console.log(stepMessage.detail["instance-id"]);
  var instanceID = stepMessage.detail["instance-id"];
  var stepevent = '{"instanceID" :"' + instanceID + '"}'
  var params = {
    stateMachineArn: process.env.STEP_FUNCTION_ARN, /* required */
    input: stepevent,
    name: 'IncidentResponse-1' + new Date().getTime()
  };
  stepfunctions.startExecution(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data);           // successful response
  });
  callback(null, 'Step Functions Successfully invoked');
};
