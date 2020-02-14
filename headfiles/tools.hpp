# ifndef _TOOLS_HPP_
# define _TOOLS_HPP_

# include <string>
# include <ctype.h>
# include <iostream>
# include "notations.hpp"
# include "events.hpp"

using std :: string;
using std :: cerr;

namespace tools {
  int to_int(string s) {
    if(s == "") return -1; 
    int ret = 0;
    for (int i = 0; i < s.length(); ++ i)
      if(isdigit(s[i])) ret = ret * 10 + s[i] - '0';
      else throw 233;
    return ret;
  }
  
  double to_double(string s) {
    double ret = 0, bse = 1.0;
    for (int i = 0; i < s.length(); ++ i) 
      if(isdigit(s[i])) {
        if(bse == 1.0) ret = ret * 10 + s[i] - '0';
        else ret = ret + bse * (s[i] - '0'), bse = bse * 0.1;
      } else if(s[i] == '.') bse = bse * 0.1;
      else throw 233;
    return ret;
  }
  
  Team to_team(string s) {
    if(s[0] == 'H') {
      return Team(Huskies);
    } else {
      int id = 0;
      for (int i = 8; i < s.length(); ++ i)
        if(isdigit(s[i])) id = id * 10 + s[i] - '0';
      return Team(Opponent, id);
    }
  }
  
  Player to_player(string s) {
    if(s == "") return Player();
    string team = "";
    int pos = 0;
    for (; pos < s.length(); ++ pos) {
      if(s[pos] == '_') break;
      team = team + s[pos];
    }
    
    PlayerPosition pp;
    ++ pos;
    if (s[pos] == 'G') pp = GK;
    else if (s[pos] == 'D') pp = DF;
    else if (s[pos] == 'M') pp = MF;
    else if (s[pos] == 'F') pp = FW;
    
    int id = 0;
    for (++ pos; pos < s.length(); ++ pos) 
      if(isdigit(s[pos])) id = id * 10 + s[pos] - '0';
    
    return Player(to_team(team), pp, id);
  }
  
  evType to_evType(string s) {
    for (int i = 0; i < 11; ++ i)
      if(s == evName[i]) return evType(i);
    return evType(0);
  }
  
  evSubType to_evSubType(string s) {
    for (int i = 0; i < 37; ++ i)
      if(s == subevName[i]) return evSubType(i);
    else return evSubType(0);
  }
}

# endif
