# include <bits/stdc++.h>
# include "../headfiles/events_reader.hpp"
# include "../headfiles/notations.hpp"
# include "../headfiles/tools.hpp"
# include "../headfiles/events.hpp"

using namespace std;

int main() {
  evReader ev_reader;
  vector <Event> el(ev_reader.parse());
  
  freopen("../data/passing_data.csv", "w", stdout);
  for (int i = 0; i < el.size(); ++ i) {
    if(el[i].type == Pass) {
      cout << el[i].matchID << ',' << (el[i].team.name == Huskies) << ',';
      if(el[i].pdst.valid) cout << "1,";
      else cout << "0,";
      el[i].eori.output_cout();
      cout << ',';
      el[i].edst.output_cout();
      cout << '\n';
    }
  }
  return 0;
}
