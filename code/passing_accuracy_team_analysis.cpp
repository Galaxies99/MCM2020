# include <bits/stdc++.h>
# include "../headfiles/events_reader.hpp"
# include "../headfiles/notations.hpp"
# include "../headfiles/tools.hpp"
# include "../headfiles/events.hpp"

using namespace std;

map <Team, pair <int, int> > acc[40];

int main() {
  evReader ev_reader;
  vector <Event> el(ev_reader.parse());
  
  for (int i = 0; i < el.size(); ++ i) {
    if(el[i].type == Pass) {
      acc[el[i].matchID][el[i].team].second ++;
      if(el[i].pdst.valid) acc[el[i].matchID][el[i].team].first ++;
    }
  }
  
  freopen("../data/passing_accuracy_team.csv", "w", stdout);
  cout << "MatchID,OurTeam,OurSuccessPass,OurTotalPass,OurAccuracy,OpponentTeam,OpponentSuccessPass,OpponentTotalPass,OpponentAccuracy\n";
  for (int i = 1; i <= 38; ++ i) {
    cout << i;
    for (map <Team, pair <int, int> > :: iterator it = acc[i].begin(); it != acc[i].end(); ++ it) {
      cout << ",";
      (it -> first).output_cout();
      int sp = (it -> second).first, tp = (it -> second).second;
      cout << ',' << sp << ',' << tp << ',' << 1.0 * sp / tp;
    } 
    cout << endl;
  }
  return 0;
}
