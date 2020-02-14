# include <bits/stdc++.h>
# include "../headfiles/events_reader.hpp"
# include "../headfiles/notations.hpp"
# include "../headfiles/tools.hpp"
# include "../headfiles/events.hpp"

using namespace std;

map <TeamName, double> possession_time[40];

int main() {
  evReader ev_reader;
  vector <Event> el(ev_reader.parse());
  
  for (int i = 0; i < el.size(); ++ i) {
    int j = i + 1;
    TeamName cur = el[i].team.name;
    for (; j < el.size() && el[i].matchID == el[j].matchID && el[i].half == el[j].half; ++ j) {
      if(el[j].team.name == cur) possession_time[el[j].matchID][cur] += el[j].tm - el[j - 1].tm;
      else cur = el[j].team.name;
    }
    i = j - 1;
  }
  
  freopen("../data/possession.csv", "w", stdout);
  cout << "MatchID,OurPossession,OurPossessionRate,OpponentPossession,OpponentPossessionRate\n";
  for (int i = 1; i <= 38; ++ i) {
    double total_time = 0.0;
    for (map <TeamName, double> :: iterator it = possession_time[i].begin(); it != possession_time[i].end(); ++ it) 
      total_time += (it -> second); 
    cout << i;
    for (map <TeamName, double> :: iterator it = possession_time[i].begin(); it != possession_time[i].end(); ++ it) {
      cout << ',' << (it -> second) << ',' << (it -> second) / total_time;
    } 
    cout << endl;
  }
  return 0;
}
