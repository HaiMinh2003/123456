# controller.py
from models import model
from views import forecast_view

def run_forecast():
    view.show_title()
    uploaded_file = view.show_file_uploader()

    if uploaded_file:
        df = model.load_data(uploaded_file)
        stock_codes = sorted(df["StockCode"].unique())
        countries = sorted(df["Country"].unique())
        
        stock_code, country, forecast_months, threshold = view.show_input_controls(
            stock_codes, countries, 3, 10
        )

        if st.button("🚀 Chạy dự báo"):
            forecast_result, forecast, recent_avg = model.forecast_revenue(
                df, stock_code, country, forecast_months
            )

            if forecast_result is None:
                view.show_warning("❌ Không có dữ liệu phù hợp.")
            else:
                forecasted_mean = forecast_result["Doanh thu dự báo"].mean()
                forecasted_min = forecast_result["Doanh thu dự báo"].min()
                forecasted_max = forecast_result["Doanh thu dự báo"].max()
                pct_total_change = (forecasted_mean - recent_avg) / recent_avg * 100

                if pct_total_change > 10:
                    trend_desc = "xu hướng TĂNG rõ rệt"
                elif pct_total_change < -10:
                    trend_desc = "xu hướng GIẢM đáng kể"
                else:
                    trend_desc = "xu hướng ỔN ĐỊNH"

                comment = (
                    f"🔍 Trong {forecast_months} tháng dự báo, "
                    f"doanh thu trung bình dự kiến đạt {forecasted_mean:.1f}, "
                    f"{'tăng' if pct_total_change >= 0 else 'giảm'} {abs(pct_total_change):.1f}% so với trung bình 3 tháng gần nhất.\n\n"
                    f"Doanh thu dự báo dao động từ {forecasted_min:.1f} đến {forecasted_max:.1f}, "
                    f"thể hiện {trend_desc}."
                )

                suggestions = []
                for _, row in forecast_result.iterrows():
                    month_label = row["Tháng dự báo"]
                    pct = row["So với TB 3T (%)"]
                    # Dựa trên % thay đổi, đưa ra hành động và gợi ý chi tiết
                    if pct >= 10:
                        trend = "📈 Tăng rất mạnh"
                        action = "Mở rộng sản xuất và tăng cường cung cấp sản phẩm.\nĐẩy mạnh các chiến dịch quảng bá và bán hàng."
                        detail = "Tăng cường quảng bá sản phẩm và mở rộng chiến dịch marketing.\nXem xét hợp tác với các KOL/KOC để mở rộng thị trường."
                    elif 5 <= pct < 10:
                        trend = "🟢 Tăng mạnh"
                        action = "Tiếp tục duy trì chiến lược marketing hiện tại.\nXem xét mở rộng sản xuất và tăng cường cung cấp sản phẩm."
                        detail = "Tiếp tục duy trì các chiến lược marketing đang hoạt động hiệu quả.\nKhám phá các thị trường mới và đầu tư vào cải tiến sản phẩm."
                    elif 0 <= pct < 5:
                        trend = "➖ Tăng nhẹ"
                        action = "Duy trì chiến lược marketing hiện tại.\nTăng cường quảng bá sản phẩm và khuyến mãi."
                        detail = "Xem xét các kênh quảng cáo hiệu quả hơn (ví dụ: TikTok, Facebook, Instagram).\nTăng cường hợp tác với các KOL/KOC."
                    elif -5 < pct < 0:
                        trend = "🔵 Giảm nhẹ"
                        action = "Cải thiện chiến lược marketing để duy trì ổn định.\nXem xét các chiến lược khuyến mãi."
                        detail = "Điều chỉnh mức giá sản phẩm để cải thiện lợi nhuận.\nTập trung vào nâng cao trải nghiệm khách hàng."
                    elif -10 < pct <= -5:
                        trend = "📉 Giảm mạnh"
                        action = "Cần thay đổi chiến lược marketing hoàn toàn để thu hút khách hàng mới.\nTăng cường các chương trình khuyến mãi mạnh mẽ."
                        detail = "Tổ chức các sự kiện bán hàng đặc biệt hoặc flash sale.\nTăng cường chiến dịch quảng cáo trực tuyến và giảm giá mạnh."
                    else:
                        trend = "🚨 Giảm rất mạnh"
                        action = "Điều chỉnh ngay lập tức chiến lược marketing.\nGiảm giá mạnh và thanh lý hàng tồn kho."
                        detail = "Cân nhắc giảm giá 10–20% hoặc thanh lý hàng tồn kho.\nTổ chức chiến dịch quảng cáo mạnh mẽ hơn và tăng ngân sách truyền thông."

                    suggestions.append(f"**{month_label}** - Xu hướng: {trend}\n- Đề xuất: {action}\n- Gợi ý chi tiết: {detail}\n")

                view.show_forecast_result(forecast_result)
                view.show_chart(forecast)
                view.show_comments(comment)
                view.show_suggestions(suggestions)

# Chạy controller
if __name__ == "__main__":
    run_forecast()
