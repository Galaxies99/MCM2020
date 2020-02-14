# include "headfiles/events_reader.hpp"
# include <bits/stdc++.h>

using namespace std;

int main() {
  evReader ev_reader;
  vector <Event> el(ev_reader.parse());
  for (int i = 0; i < el.size(); ++ i) {
    el[i].output_cout();
    system("pause");
  }
}
