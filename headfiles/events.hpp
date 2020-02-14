# ifndef _EVENTS_HPP_
# define _EVENTS_HPP_

# include "notations.hpp"
# include <iostream>

using std :: cout;

struct Team {
  TeamName name;
  int id;
  
  Team() = default;
  Team(TeamName name, int id = 0) : name(name), id(id) {}
  ~ Team() = default;
  
  void output_cout() {
    if(name == Huskies) cout << "Huskies";
    if(name == Opponent) cout << "Opponent" << id;
  }
};

struct Player {
  Team team;
  PlayerPosition pos;
  int id;
  bool valid;
  
  Player() { valid = false; }
  Player(Team team, PlayerPosition pos, int id) : team(team), pos(pos), id(id) { valid = true; }
  ~ Player() = default;
  
  void output_cout() {
    if(valid) {
      team.output_cout();
      if(pos == GK) cout << "G";
      if(pos == DF) cout << "D";
      if(pos == MF) cout << "M";
      if(pos == FW) cout << "F";
      cout << id;
    }
  }
};

struct Coordinates {
  double x, y;
  bool valid;
  
  Coordinates() { valid = false; }
  Coordinates(double x, double y) : x(x), y(y) { valid = true; }
  ~ Coordinates() = default;
  
  void output_cout() {
    if(valid) cout << x << ',' << y;
  }
};

struct Event {
  int matchID;            // matchID
  Team team;              // teamID
  Player pori, pdst;      // origin player, destination player
  int half;               // match period
  double tm;              // time
  evType type;            // event type
  evSubType subtype;      // event subtype
  Coordinates eori, edst; // event origin coordinates, event origin coordinates
  
  Event() = default;
  Event(int matchID, Team team, Player pori, Player pdst, int half, double tm, evType type, evSubType subtype, Coordinates eori, Coordinates edst) :
    matchID(matchID), team(team), pori(pori), pdst(pdst), half(half), tm(tm), type(type), subtype(subtype), eori(eori), edst(edst) {} 
  ~ Event() = default; 
  
  void output_cout() {
    cout << matchID << ',';
    team.output_cout();
    cout << ',';
    pori.output_cout();
    cout << ',';
    pdst.output_cout();
    cout << half << "H," << tm << ',';
    cout << evName[type] << ',' << subevName[subtype] << ',';
    eori.output_cout(); 
    cout << ',';
    edst.output_cout();
    cout << '\n';
  }
};

# endif
