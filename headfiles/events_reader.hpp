# ifndef _EVENTS_READER_
# define _EVENTS_READER_

# include <vector>
# include <string>
# include <iostream>
# include "tools.hpp"
# include "events.hpp"
# include "notations.hpp"

using std :: cerr;
using std :: vector;

struct evReader {
  FILE *fp;
  char str[1010];
  
  evReader() {
    fp = fopen("../data/fullevents.csv", "r");
  }
  
  vector <Event> parse() {
    int eid = 0;
    vector <Event> ret; 
    ret.clear();
    
    while(fgets(str, 1010, fp)) {
      ++ eid;
      if(eid == 1) continue;
      
      Event e;
      
      string s = "";
      int pos = 0;
      for (; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.matchID = tools :: to_int(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.team = tools :: to_team(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.pori = tools :: to_player(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.pdst = tools :: to_player(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      if(s[0] == '1') e.half = 1;
      else if(s[0] == '2') e.half = 2;
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.tm = tools :: to_double(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.type = tools :: to_evType(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      e.subtype = tools :: to_evSubType(s);
      
      double x, y;
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      x = tools :: to_double(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      y = tools :: to_double(s);
      
      if(x == -1 || y == -1) e.eori = Coordinates();
      else e.eori = Coordinates(x, y);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',') break;
        s = s + str[pos];
      }
      x = tools :: to_double(s);
      
      for (s = "", ++ pos; str[pos]; ++ pos) {
        if(str[pos] == ',' || str[pos] == '\n' || str[pos] == '\t') break;
        s = s + str[pos];
      }
      y = tools :: to_double(s);
      
      if(x == -1 || y == -1) e.edst = Coordinates();
      else e.edst = Coordinates(x, y);
      
      ret.push_back(e);  
    }
    return ret;
  }
  
  ~ evReader() {
    if(fp != nullptr) fclose(fp);
  } 
};

# endif
