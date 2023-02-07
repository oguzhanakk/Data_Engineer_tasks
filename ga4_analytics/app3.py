"""Analytics Data API Beta V1."""
import os
import csv
from dotenv import load_dotenv
import httplib2
from google.analytics import data_v1beta
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    Filter
)

from apiclient.discovery import build
#from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
import google.oauth2.credentials


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN= os.getenv("REFRESH_TOKEN")
VIEW_ID = os.getenv("VIEW_ID") # Raw / Unfiltered View
PROPERTY_ID = "properties/" + str( os.getenv("PROPERTY_ID"))
start_date = "2022-10-01"
end_date = "2022-10-03"
event_name = "screen_view"

#dimensions = ['eventName', 'unifiedScreenClass', 'appVersion', 'firstSessionDate', 'sessionSourceMedium', 'customEvent:storyID', "customEvent:pn_id" , "customEvent:method[sign_up]" ,'customUser:user_id']
#metrics = ['eventCount', 'screenPageViews','sessions','totalUsers','newUsers','conversions','engagementRate']
dimensions = ['eventName', 'unifiedScreenClass', 'appVersion', 'dateHour', 'sessionSourceMedium', 'customEvent:storyID', "customEvent:pn_id" , "customEvent:method[sign_up]" ,'customUser:user_id']
metrics = ['eventCount']
events = [ "screen_view", "view_home", "user_engagement", "view_wallet", "notification_receive", "notification_dismiss", "access_token_error_android", "session_start", "view_redeem", "code_submit", "points_win", "view_promo", "code_entry_error", "view_prize", "wallet_redeem", "view_profile", "redeem_prize", "story_open", "page_view", "wallet_claim_prize", "login", "first_open", "access_token_error_ios", "app_remove", "not_enough_point", "sign_up", "age_verification", "promo_win", "scan_onboarding", "pn_open", "notification_open", "log_out", "story_engagement", "os_update", "app_exception", "app_update", "scan_start", "notification_foreground", "first_visit", "view_receipt", "app_clear_data", "scan_submit", "support_message_sent", "scan_verification", "point_redeem", "scan_error", "account_deleted_info"]

print("VIEW_ID",VIEW_ID)
print("PROPERTY_ID",PROPERTY_ID)
print("CLIENT_ID",CLIENT_ID)
print("CLIENT_SECRET",CLIENT_SECRET)
print("REFRESH_TOKEN",REFRESH_TOKEN)
print("start_date",start_date)
print("end_date",end_date)
print("event_name",event_name)


def worker(start_date=start_date,end_date=end_date,event_name=event_name):

    from datetime import date, timedelta, datetime

    obj_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    obj_end_date = datetime.strptime(end_date, "%Y-%m-%d")

    credentials = google.oauth2.credentials.Credentials(
        token=None,  # =None,  # set access_token to None since we use a refresh token
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN,
        token_uri=GOOGLE_TOKEN_URI)


    with open(f'data-{start_date}-{end_date}.csv', 'a+', encoding='UTF8', newline='') as f:

        writer = csv.writer(f)
        # writer.writerow(headers) #append olacağı için headeri kaldırdım.

        while obj_start_date <= obj_end_date:
            print(obj_start_date.strftime("%Y-%m-%d"))

            dataclient = data_v1beta.BetaAnalyticsDataClient(credentials=credentials)
            all_data = []
            offset = 0
            totalrow = 1
            limit = 100000
            x = 1

            date = obj_start_date.strftime("%Y-%m-%d")

            while offset < totalrow:
                request = RunReportRequest(
                    property=PROPERTY_ID,
                    dimensions=[Dimension(name=dimension) for dimension in dimensions],
                    metrics=[Metric(name=metric) for metric in metrics],
                    date_ranges=[DateRange(start_date=date, end_date=date)],
                    limit=limit,
                    offset=offset,
                    # dimension_filter=FilterExpression(
                    #     filter=Filter(
                    #         field_name="eventName",
                    #         string_filter=Filter.StringFilter(value=event_name),
                    #     )
                    # ),
                )
                response = dataclient.run_report(request)
                totalrow = response.row_count
                print(f"row count: {x}  {response.row_count}")
                x += 1

                # # Handle the response
                # headers = []
                # headers = [header.name for header in response.dimension_headers]
                # headers += [header.name for header in response.metric_headers]
                # print(headers)

                raw_rows = []
                for row in response.rows:
                    raw_row = []
                    raw_row = [content.value for content in row.dimension_values]
                    raw_row += [content.value for content in row.metric_values]
                    raw_rows.append(raw_row)
                    all_data.append(raw_row)
                offset += limit
                all_data.append(raw_rows)

                writer.writerows(raw_rows) #raw_rows'lari excell'e basiyor (limit=100 olursa 100'er 100'er)

                print(len(all_data)) #all_data ile isimiz kalmadi tek tek bastigimiz icin fakat toplam data kaciyor mu diye gormek icin
                                    #all_data append kismi tutularak kontrol saglanabilir.
                                    #eski programdaki len(all_data) = burdaki len(all_data) olursa veri kacmiyor demektir.
                                    #len(all_Data) her dongude 1 fazla gosteriyor onemli degil.


            obj_start_date += timedelta(days=1)

def main():
    worker("2022-09-01","2022-10-01","account_deleted_info") #TODO: burayı dışardan argüman alacak şekilde düzenle
    #TODO: limiti 100k yap, event bazlı istek at. pagination dene offset ile
if __name__ == '__main__':
  main()
