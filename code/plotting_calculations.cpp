# include <bits/stdc++.h>
# include "../headfiles/events_reader.hpp"
# include "../headfiles/notations.hpp"
# include "../headfiles/tools.hpp"
# include "../headfiles/events.hpp"

using namespace std;

map <Player, pair <Coordinates, double> > mp[40];
map <Player, bool> sub[40];
void add_coordinate(int i, Player p, Coordinates c, double d) {
  if(mp[i].find(p) == mp[i].end()) mp[i][p] = make_pair(c, d);
  else {
    pair <Coordinates, double> cur = mp[i][p];
    mp[i][p] = make_pair(cur.first + c, cur.second + d);
  }
}

int main() {
  evReader ev_reader;
  vector <Event> el(ev_reader.parse());
  
  for (int i = 0; i < el.size(); ++ i) {
    switch(el[i].type) {
      case Pass:
        add_coordinate(el[i].matchID, el[i].pori, el[i].eori, 1);
        if(el[i].pori != el[i].pdst && el[i].pdst.valid) 
          add_coordinate(el[i].matchID, el[i].pdst, el[i].edst, 1);
        break;
      case Goalkeeper_leaving_line:
      case Save_attempt:
        add_coordinate(el[i].matchID, el[i].pori, Coordinates(0, 50), 1);
        break;
      case Duel:
      case Others_on_the_ball:
      case Foul:
      case Offside:
      case Shot:
        add_coordinate(el[i].matchID, el[i].pori, el[i].eori, 1);
        break;
      case Substitution:
        sub[el[i].matchID][el[i].pdst] = 1;
      default: break;
    }
  }
  
  freopen("../data/plotting_data.csv", "w", stdout);
  cout << "MatchID,Player,PlayerAverageX,PlayerAverageY,CountValue,isSubstitution\n";
  for (int i = 1; i <= 38; ++ i) {
    for (map <Player, pair <Coordinates, double> > :: iterator it = mp[i].begin(); it != mp[i].end(); ++ it) {
      pair <Coordinates, double> res = (it -> second);
      cout << i << ',';
      (it -> first).output_cout();
      cout << ',';
      res.first = res.first / res.second;
      if((it -> first).team.name == Opponent)
        res.first = Coordinates(100 - res.first.x, 100 - res.first.y);
      res.first.output_cout();
      cout << ',' << res.second << ',' << sub[i][it -> first] << '\n'; 
    }
  }
  
  return 0;
}
