import os
import file_manager
import data_converter
import chart_generator
import pdf_generator
import database_manager

def main():
    print("=== Cricket Match Stats Manager ===")
    
    data_dir = 'data'
    output_dir = 'output'
    charts_dir = 'charts'
    reports_dir = 'reports'
    
    # Source JSON file
    source_json = os.path.join(data_dir, 'match_stats.json')
    
    # Output files
    excel_file = os.path.join(output_dir, 'match_stats.xlsx')
    csv_file = os.path.join(output_dir, 'match_stats.csv')
    imported_json = os.path.join(output_dir, 'imported_from_csv.json')
    copied_json = os.path.join(output_dir, 'copied_match_stats.json')
    renamed_json = os.path.join(output_dir, 'renamed_match_stats.json')
    updated_json = os.path.join(output_dir, 'updated_match_stats.json')
    pdf_file = os.path.join(reports_dir, 'india_vs_australia_2023_final_report.pdf')

    print("\n--- 1. JSON to Table Generation ---")
    data_converter.display_tables_from_json(source_json)
    
    print("\n--- 2. JSON to Excel & CSV Generation ---")
    data_converter.json_to_excel(source_json, excel_file)
    data_converter.json_to_csv(source_json, csv_file)
    
    print("\n--- 3. Read CSV and Generate JSON ---")
    data_converter.csv_to_json(csv_file, imported_json)
    
    print("\n--- 4. File Operations ---")
    # Copy file to output directory
    file_manager.copy_file(source_json, copied_json)
    
    # Rename the copied file
    file_manager.rename_file(copied_json, renamed_json)

    # Copy the renamed file to a new file for updates
    file_manager.copy_file(renamed_json, updated_json)
    
    # Update a specific value (e.g. changing venue)
    file_manager.update_json_value(updated_json, ['match_details', 'venue'], 'Narendra Modi Stadium, Ahmedabad (Updated)')
    
    # Append new data (e.g. adding a new bowler for India)
    new_bowler = {"bowler": "Kuldeep Yadav", "wickets": 0}
    data = file_manager.read_json(updated_json)
    if data:
        data['bowling_stats']['India'].append(new_bowler)
        file_manager.save_json(data, updated_json)
        print("Appended new bowler to India in updated JSON.")
    
    # Delete the imported JSON file to demonstrate deletion
    file_manager.delete_file(imported_json)
    
    print("\n--- 5. Generate Charts from Data ---")
    chart_generator.generate_charts(source_json, charts_dir)
    
    print("\n--- 6. Generate PDF File ---")
    pdf_generator.generate_pdf_report(source_json, charts_dir, pdf_file)
    
    print("\n--- 7. MySQL Database Integration ---")
    connection = database_manager.connect_db()
    if not connection:
        print("MySQL connection failed. Please check DB_CONFIG in database_manager.py.")
        print("Skipping Step 7 database operations.")
    else:
        connection.close() # Close test connection
        try:
            database_manager.create_database_if_not_exists()
            database_manager.reset_database_tables()
            database_manager.create_tables()
            
            # Insert data
            match_id = database_manager.insert_match_data_from_json(source_json)
            
            # Display matches
            matches = database_manager.get_all_matches()
            if matches:
                print("\nMatches:")
                for m in matches:
                    print(m)
                    
            # Display team scores
            team_scores = database_manager.get_team_scores()
            if team_scores:
                print("\nTeam Scores:")
                for ts in team_scores:
                    print(ts)
                    
            # Display batting stats
            batting_stats = database_manager.get_batting_stats()
            if batting_stats:
                print("\nBatting Stats:")
                for b in batting_stats:
                    print(b)
                    
            # Display bowling stats
            bowling_stats = database_manager.get_bowling_stats()
            if bowling_stats:
                print("\nBowling Stats:")
                for b in bowling_stats:
                    print(b)
                
            # Export data
            database_manager.export_db_to_json()
            database_manager.export_db_to_excel()
            database_manager.generate_html_table()
            
        except Exception as e:
            print(f"Database integration skipped or failed: {e}")
    
    print("\n=== All Tasks Completed Successfully! ===")

if __name__ == "__main__":
    main()
