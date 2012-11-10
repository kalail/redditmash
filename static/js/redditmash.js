var leftVoteButton;
var rightVoteButton;
var nameField;
var messageField;
var channel;
var hasBroadcastedJoined = false;
var lastInsertedMessageTime = new Date(0);

$(document).ready(function() {
  // set up the event handlers for the voting buttons
  leftVoteButton = $("#left-vote-button");
  rightVoteButton = $("#right-vote-button");
  leftVoteButton.click(leftVoteButtonClicked);
  rightVoteButton.click(rightVoteButtonClicked);
  // set up the event handlers for the chat boxes
  // also enables validation on when the user is allowed to send a message
  nameField = $(".chat-input-name");
  messageField = $(".chat-input");
  nameField.keypress(onNameChanged);
  nameField.blur(onNameChanged);
  messageField.keypress(onMessageChanged);
  // disable the message box by default until they enter a name
  messageField.attr("disabled", "true");
  messageField.attr("placeholder", "Enter a name to continue");
  try
  {
    channel = connect();
  } catch(ReferenceError) { }

  // adds pseudo classes to the post titles. Because they are created dynamically
  // in pseudo classes, they must be added with javascript
  $('i').each(function(idx) {
    if($(this).data('css') != null)
      document.styleSheets[0].insertRule('.'  + $(this).data('css') + ':after { content: "' + $(this).data('title').replace(/-/g, ' ') + '"; font-size: 3px}', 0);
      if($(this).data('title').length > 40)
      {
        // document.styleSheets[0].insertRule('.'  + $(this).data('css') + ':after { font-size: 5px; }', 0);
      }
  });

  // adds highlight to navbar link
  if(/rankings/.exec(window.location.pathname))
  {
    $("#navbar-compare").addClass("selected");
    $("#navbar-rankings").addClass("deselected");
  } else {
    $("#navbar-rankings").addClass("selected");
    $("#navbar-compare").addClass("deselected");
  }


});

$(window).load(function() {
  // horizontally center landscape pictures
  // this has to be done in js because the top margin of the image has to be set dynamically based on how tall it is
  // It doesn't work well because all the pictures load and then spring into place
  // $(".cbimg").each(function(i) { if($(this).width() > $(this).height()) { $(this).css('margin-top', (432 - parseInt($(".cbimg:eq(1)").css('height')))/3 + 'px') } });

})

// attempt to connect to imo
function connect() {
  var client = {
    connect: onConnect,
    event_queue: onMessage
  };
  return new IMO.Channel(client);
}

function onConnect() {
  channel.subscribe([{"type": "event_queue", "name": "redditmash"}], 0);
}

function onMessage(name, event) {
  var messageTime = new Date(0);
  messageTime.setUTCSeconds(event.timestamp);
  if(messageTime.getMinutes() != lastInsertedMessageTime.getMinutes()) {
    insertTimeMessage(messageTime.toLocaleTimeString());
  }
  lastInsertedMessageTime = messageTime;
  insertChatMessage(event.object.message);
}

function onNameChanged(event) {
  if(!hasBroadcastedJoined && nameField.val() != "" && (event.keyCode == 13 || event.type == "blur")) {
    hasBroadcastedJoined = true;
    channel.event_queue(
      "redditmash",
      {"object": {"message": nameField.val() + " joined the chat."}}
    );
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
  if(messageField.val() != "" && event.keyCode == 13) {
    channel.event_queue(
      "redditmash",
      {"object": {"message": nameField.val() + ": " + messageField.val()}}
    );
    messageField.val("");
    return false;
  }

  return event.keyCode != 13;
}

function insertChatMessage(message) {
  $('.chat-table > tbody:last').append('<tr><td>' + message + '</td></tr>');
  $(".chat-div:eq(0)").scrollTop(999999);
}

function insertTimeMessage(message) {
  $('.chat-table > tbody:last').append('<tr><td class="chat-time-message">' + message + '</td></tr>');
  $(".chat-div:eq(0)").scrollTop(999999);
}


function leftVoteButtonClicked() {
  submitVote(leftVoteButton, $("body").data("post-1-id"));
  return false;
}

function rightVoteButtonClicked() {
  submitVote(rightVoteButton, $("body").data("post-2-id"));
  return false;
}

function submitVote(button, id) {
  $.ajaxSetup ({
        cache: false
  });
  var ajax_load = '<img src="/static/img/loader.gif" alt="Loading..." style="width: 24px">';
  //  load() functions
  var loadUrl = "/index";
  button.html(ajax_load).load(function(response, status, xhr) {
    if (status == "error") {
      var msg = "Sorry but there was an error: ";
      $("#error").html(msg + xhr.status + " " + xhr.statusText);
    } else {
      window.loation.reload();
    }
  });
}

String.prototype.toHHMMSS = function () {
    sec_numb    = parseInt(this);
    var hours   = Math.floor(sec_numb / 3600);
    var minutes = Math.floor((sec_numb - (hours * 3600)) / 60);
    var seconds = sec_numb - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    var time    = hours+':'+minutes+':'+seconds;
    return time;
}
