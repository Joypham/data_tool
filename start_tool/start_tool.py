import time

if __name__ == "__main__":
    start_time = time.time()

    # Artist_page check_box:
    #     from tools.artistpage_justin import check_box
    #     check_box()

    # Extract artist_name for collecting from youtube
    from tools.daily_export_artist_contribution import export_artist_contribution

    export_artist_contribution()

    print("--- %s seconds ---" % (time.time() - start_time))
