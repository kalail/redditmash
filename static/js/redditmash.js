var leftVoteButton;
var rightVoteButton;
var nameField;
var messageField;
var channel;
var hasBroadcastedJoined = false;

$(document).ready(function() {
  leftVoteButton = $("#left-vote-button");
  rightVoteButton = $("#right-vote-button");
  leftVoteButton.click(leftVoteButtonClicked);
  rightVoteButton.click(rightVoteButtonClicked);

  nameField = $(".chat-input-name");
  messageField = $(".chat-input");
  nameField.keypress(onNameChanged);
  nameField.blur(onNameChanged);
  messageField.keypress(onMessageChanged);
  messageField.attr("disabled", "true");
  messageField.attr("placeholder", "Enter a name to continue");

  channel = connect();
});

function connect() {
  var client = {
    connect: onConnect
  };
  return new IMO.Channel(client);
}

function onConnect() {
  // channel.subscribe([{"type": "event_queue", "name": "redditmash"}], 0);
}

function onNameChanged(event) {
  if(!hasBroadcastedJoined && nameField.val() != "" && (event.keyCode == 13 || event.type == "blur")) {
    hasBroadcastedJoined = true;
    channel.event_queue(
      "redditmash",
      {"object": {"message": nameField.val() + " joined the chat."}}
    );
    alert('Broadcasted Join');
  }
  if(nameField.val() == "") {
    messageField.attr("disabled", "");
    messageField.attr("placeholder", "Enter a name to continue");
  } else
  {
    messageField.removeAttr("disabled");
    messageField.attr("placeholder", "Message");
  }
  if(event.keyCode == 13) {
    return false;
  }
}

function onMessageChanged(event) {

}

function leftVoteButtonClicked() {
  return false;
}

function rightVoteButtonClicked() {
  return false;
}
