import re
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

FINANCIAL_DATA = {
    'apple': {
        'revenue': {
            '2023': '$383.29B',
            '2024': '$391.04B',
            '2025': '~$400.00B (Est)',
        },
        'net_income': {
            '2023': '$96.99B',
            '2024': '$93.74B',
            '2025': '~$100.00B (Est)',
        },
        'assets': {
            '2023': '$352.58B',
            '2024': '$364.98B',
            '2025': '~$375.00B (Est)',
        },
        'liabilities': {
            '2023': '$290.44B',
            '2024': '$298.00B',
            '2025': '~$300.00B (Est)',
        },
        'cash_flow': {
            '2023': '$110.54B',
            '2024': '$118.25B',
            '2025': '~$120.00B (Est)',
        },
    },
    'microsoft': {
        'revenue': {
            '2023': '$211.91B',
            '2024': '$245.12B',
            '2025': '~$270.00B (Est)',
        },
        'net_income': {
            '2023': '$72.36B',
            '2024': '$88.14B',
            '2025': '~$95.00B (Est)',
        },
        'assets': {
            '2023': '$411.98B',
            '2024': '$512.16B',
            '2025': '~$560.00B (Est)',
        },
        'liabilities': {
            '2023': '$205.75B',
            '2024': '$243.69B',
            '2025': '~$270.00B (Est)',
        },
        'cash_flow': {
            '2023': '$87.58B',
            '2024': '$118.55B',
            '2025': '~$125.00B (Est)',
        },
    },
    'tesla': {
        'revenue': {
            '2023': '$96.77B',
            '2024': '$97.71B',
            '2025': '~$102.00B (Est)',
        },
        'net_income': {
            '2023': '$14.99B',
            '2024': '$7.10B',
            '2025': '~$9.50B (Est)',
        },
        'assets': {
            '2023': '$106.62B',
            '2024': '$119.80B',
            '2025': '~$130.00B (Est)',
        },
        'liabilities': {
            '2023': '$43.01B',
            '2024': '$46.80B',
            '2025': '~$50.00B (Est)',
        },
        'cash_flow': {
            '2023': '$13.25B',
            '2024': '$14.85B',
            '2025': '~$17.00B (Est)',
        },
    },
}
KEYWORDS_COMPANY = {
    'apple': ['apple', 'appl', 'aapl', 'أبل', 'ابل'],
    'microsoft': ['microsoft','mcrosoft', 'msft', 'مايكروسوفت'],
    'tesla': ['tesla', 'tsla', 'تيسلا', 'تسلا'],
}

KEYWORDS_METRIC = {
    'revenue': ['revenue', 'sales', 'إيرادات', 'مبيعات', 'المبيعات', 'الإيرادات'],
    'net_income': [
        'net income',
        'profit',
        'earnings',
        'أرباح',
        'دخل',
        'صافي',
        'أرباحها',],
    'assets': ['asset', 'assets', 'أصول', 'الأصول'],
    
    'liabilities': [
        'liability',
        'liabilities',
        'debt',
        'debts',
        'ديون',
        'التزامات',
        'الالتزامات',],
    'cash_flow': ['cash flow', 'cash', 'تدفق', 'نقدي', 'التدفقات'],
}


def parse_query(user_query: str):
  query = user_query.lower()

  found_companies = []
  for company, aliases in KEYWORDS_COMPANY.items():
    if any(alias in query for alias in aliases):
      found_companies.append(company)

  found_metric = None
  for metric, aliases in KEYWORDS_METRIC.items():
    if any(alias in query for alias in aliases):
      found_metric = metric
      break

  year_match = re.search(r'\b(2023|2024|2025)\b', query)
  found_year = year_match.group(1) if year_match else '2024'

  is_compare = any(
      k in query
      for k in [
          'compare',
          'vs',
          'versus',
          'highest',
          'lowest',
          'best',
          'مقارنة',
          'أعلى',
          'أقل', ] )
  is_summary = any(
      k in query for k in ['summary', 'overview', 'report', 'ملخص', 'تقرير'])
  is_trend = any(
      k in query for k in ['trend', 'growth', 'change', 'نمو', 'تغير', 'تطور'])

  return found_companies, found_metric, found_year, is_compare, is_summary, is_trend


def get_chatbot_response(user_query: str) -> str:
  companies, metric, year, is_compare, is_summary, is_trend = parse_query(
      user_query)
  if is_summary and companies:
    c = companies[0]
    data = FINANCIAL_DATA[c]
    return (
        f"📊 **{c.capitalize()} ({year}) Summary**:\n"
        f"- Revenue: {data['revenue'][year]}\n"
        f"- Net Income: {data['net_income'][year]}\n"
        f"- Total Assets: {data['assets'][year]}\n"
        f"- Total Liabilities: {data['liabilities'][year]}\n"
        f"- Cash Flow: {data['cash_flow'][year]}")

  if is_compare:
    if 'highest' in user_query or 'best' in user_query or 'أعلى' in user_query:
      return (
          f"🏆 **Apple** generated the highest Revenue in {year} ($391.04B),"
          " while **Microsoft** achieved the highest Net Income growth"
          " (+21.80%).")
    elif 'lowest' in user_query or 'أقل' in user_query:
      return (
          f"📉 **Tesla** holds the lowest Total Liabilities among all three"
          f" companies in {year} ($46.80B).")
    elif len(companies) >= 2 and metric:
      c1, c2 = companies[0], companies[1]
      v1 = FINANCIAL_DATA[c1][metric][year]
      v2 = FINANCIAL_DATA[c2][metric][year]
      metric_name = metric.replace('_', ' ').capitalize()
      return (
          f"⚖️ **Comparison ({year} {metric_name})**:\n- {c1.capitalize()}:"
          f" {v1}\n- {c2.capitalize()}: {v2}")

  if is_trend and companies and metric:
    c = companies[0]
    data = FINANCIAL_DATA[c][metric]
    metric_name = metric.replace('_', ' ').capitalize()
    return (
        f"📈 **{c.capitalize()} {metric_name} Trend**:\n"
        f"- 2023: {data['2023']}\n"
        f"- 2024: {data['2024']}\n"
        f"- 2025: {data['2025']}")

  if companies and metric:
    c = companies[0]
    val = FINANCIAL_DATA[c][metric][year]
    metric_name = metric.replace('_', ' ').capitalize()
    return f"The {metric_name} for **{c.capitalize()}** in {year} was **{val}**."

  if metric:
    metric_name = metric.replace('_', ' ').capitalize()
    return (
        f"📋 **{metric_name} ({year}) for all companies**:\n"
        f"- Apple: {FINANCIAL_DATA['apple'][metric][year]}\n"
        f"- Microsoft: {FINANCIAL_DATA['microsoft'][metric][year]}\n"
        f"- Tesla: {FINANCIAL_DATA['tesla'][metric][year]}")

  return (
      "I couldn't detect a specific query. Try asking:\n"
      "1. 'What is Apple's revenue in 2023?'\n"
      "2. 'Compare net income between Microsoft and Tesla in 2024'\n"
      "3. 'Show me Tesla's revenue trend'\n"
      "4. 'Give me a summary for Microsoft'")

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
  data = request.get_json(silent=True) or {}
  user_query = data.get('query', '')
  bot_reply = get_chatbot_response(user_query)
  return jsonify({'response': bot_reply})


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)