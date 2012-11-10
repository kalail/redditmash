var leftVoteButton;
var rightVoteButton;

$(document).ready(function() {
  leftVoteButton = $("#left-vote-button");
  rightVoteButton = $("#right-vote-button");
  leftVoteButton.click(leftVoteButtonClicked);
  rightVoteButton.click(rightVoteButtonClicked);
});

function leftVoteButtonClicked()
{
  return false;
}

function rightVoteButtonClicked()
{
  return false;
}
