import matplotlib.pyplot as plt # type: ignore (if still unresolvable, but it should be fine now)
import pandas as pd
from file_manager import read_json
import os

def generate_charts(json_file, charts_dir):
    """Generate and save charts based on the JSON data."""
    data = read_json(json_file)
    if not data:
        return

    # Ensure charts directory exists
    os.makedirs(charts_dir, exist_ok=True)

    # 1. Bar Chart: Team Scores
    teams = list(data['team_scores'].keys())
    scores = [data['team_scores'][team]['runs'] for team in teams]
    
    plt.figure(figsize=(8, 5))
    colors = ['blue', 'yellow']
    plt.bar(teams, scores, color=colors)
    plt.title('Team Scores')
    plt.ylabel('Runs')
    for i, v in enumerate(scores):
        plt.text(i, v + 2, str(v), ha='center', fontweight='bold')
    score_chart_path = os.path.join(charts_dir, 'team_score_chart.png')
    plt.savefig(score_chart_path)
    plt.close()
    print(f"Saved {score_chart_path}")

    # 2. Pie Chart: Indian Top Batsmen Contribution
    ind_bat_df = pd.DataFrame(data['batting_stats']['India'])
    labels = ind_bat_df['player']
    sizes = ind_bat_df['runs']
    
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Batting Contribution (Top Indian Batsmen)')
    ind_pie_chart_path = os.path.join(charts_dir, 'india_batting_contribution_pie_chart.png')
    plt.savefig(ind_pie_chart_path)
    plt.close()
    print(f"Saved {ind_pie_chart_path}")

    # 3. Pie Chart: Australian Top Batsmen Contribution
    aus_bat_df = pd.DataFrame(data['batting_stats']['Australia'])
    labels = aus_bat_df['player']
    sizes = aus_bat_df['runs']
    
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
    plt.title('Batting Contribution (Top Australian Batsmen)')
    aus_pie_chart_path = os.path.join(charts_dir, 'australia_batting_contribution_pie_chart.png')
    plt.savefig(aus_pie_chart_path)
    plt.close()
    print(f"Saved {aus_pie_chart_path}")

    # 4. Bar Chart: Wickets by Australian Bowlers
    aus_bowl_df = pd.DataFrame(data['bowling_stats']['Australia'])
    bowlers = aus_bowl_df['bowler']
    wickets = aus_bowl_df['wickets']
    
    plt.figure(figsize=(10, 5))
    plt.bar(bowlers, wickets, color='green')
    plt.title('Wickets Taken by Australian Bowlers')
    plt.xlabel('Bowlers')
    plt.ylabel('Wickets')
    plt.yticks(range(0, max(wickets) + 2))
    for i, v in enumerate(wickets):
        plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    
    aus_bowling_chart_path = os.path.join(charts_dir, 'australia_bowling_wickets_chart.png')
    plt.savefig(aus_bowling_chart_path)
    plt.close()
    print(f"Saved {aus_bowling_chart_path}")

    # 5. Bar Chart: Wickets by Indian Bowlers
    ind_bowl_df = pd.DataFrame(data['bowling_stats']['India'])
    bowlers = ind_bowl_df['bowler']
    wickets = ind_bowl_df['wickets']
    
    plt.figure(figsize=(10, 5))
    plt.bar(bowlers, wickets, color='blue')
    plt.title('Wickets Taken by Indian Bowlers')
    plt.xlabel('Bowlers')
    plt.ylabel('Wickets')
    if not wickets.empty:
        plt.yticks(range(0, max(wickets) + 2))
    for i, v in enumerate(wickets):
        plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    
    ind_bowling_chart_path = os.path.join(charts_dir, 'india_bowling_wickets_chart.png')
    plt.savefig(ind_bowling_chart_path)
    plt.close()
    print(f"Saved {ind_bowling_chart_path}")
