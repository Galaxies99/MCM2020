# ifndef _NOTATIONS_HPP_
# define _NOTATIONS_HPP_

# include <string>

using std :: string;

enum TeamName { Huskies, Opponent };

enum PlayerPosition { GK, DF, MF, FW };

enum evType {
  Free_Kick = 0,
  Duel,
  Pass,
  Others_on_the_ball,
  Foul,
  Goalkeeper_leaving_line,
  Offside,
  Save_attempt,
  Shot,
  Substitution,
  Interruption
};

string evName [] = {
  "Free Kick", 
  "Duel", 
  "Pass", 
  "Others on the ball", 
  "Foul", 
  "Goalkeeper leaving line", 
  "Offside",
  "Save attempt", 
  "Shot", 
  "Substitution", 
  "Interruption"
};

enum evSubType {
  sGoal_kick = 0,
  sAir_duel,
  sThrow_in,
  sHead_pass,
  sGround_loose_ball_duel,
  sSimple_pass,
  sLaunch,
  sHigh_pass,
  sTouch,
  sGround_defending_duel,
  sHand_pass,
  sGround_attacking_duel,
  sFoul,
  sFree_kick_cross,
  sGoalkeeper_leaving_line,
  sEmpty,
  sFree_kick,
  sSmart_pass,
  sCross,
  sSave_attempt,
  sCorner,
  sClearance,
  sShot,
  sAcceleration,
  sReflexes,
  sSubstitution,
  sLate_card_foul,
  sSimulation,
  sFree_kick_shot,
  sProtest,
  sHand_foul,
  sPenalty,
  sViolent_foul,
  sWhistle,
  sOut_of_game_foul,
  sBall_out_of_field,
  sTime_lost_foul
};

string subevName[] = {
  "Goal kick", 
  "Air duel", 
  "Throw in", 
  "Head pass", 
  "Ground loose ball duel", 
  "Simple pass", 
  "Launch", 
  "High pass", 
  "Touch", 
  "Ground defending duel", 
  "Hand pass", 
  "Ground attacking duel", 
  "Foul", 
  "Free kick cross", 
  "Goalkeeper leaving line", 
  "",
  "Free Kick", 
  "Smart pass", 
  "Cross", 
  "Save attempt", 
  "Corner", 
  "Clearance", 
  "Shot", 
  "Acceleration", 
  "Reflexes", 
  "Substitution", 
  "Late card foul", 
  "Simulation", 
  "Free kick shot", 
  "Protest", 
  "Hand foul", 
  "Penalty", 
  "Violent Foul", 
  "Whistle", 
  "Out of game foul", 
  "Ball out of the field", 
  "Time lost foul"
};

# endif
