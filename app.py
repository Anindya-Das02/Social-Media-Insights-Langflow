import streamlit as st
import requests

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "2d177e5d-1a7f-4135-8056-5328f241699f"
APPLICATION_TOKEN = "AstraCS:YYzArbcZDzauRlngJvRxickR:d4a27dd75057d162e88ca482f4313334bb05fcced72a1e2bc825282dd2a87b8d"
ENDPOINT = "analyze-post"

post_type_list = ["Static-images", "Carousel-posts", "Stories", "Reels", "IG-Live", "Text-Only", "Infographics"]

def build_post_type_exclusion_query(exclude_pt:str) -> str :
    return ', '.join(item for item in post_type_list if item.lower() != exclude_pt.lower())

def get_analysis_result(post_type : str) -> str:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    message = f"compare {post_type} with other post types such as {build_post_type_exclusion_query(post_type)}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)

    print(f"response status: {response.status_code}")       # Debug purpose

    result = None
    if response.status_code == 200:
        response_json = response.json()
        result = response_json["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    return result


def main():
    st.title("📊 Posts Analysis & Insights")
    st.markdown("---")

    post_type = st.selectbox("Select post type to analyze:", post_type_list)

    buttonAction = st.button("Submit")

    if buttonAction:
        try:
            with st.spinner("Analyzing..."):
                analysis_result = get_analysis_result(post_type)
                if analysis_result:
                    st.subheader("🔎 Key Insights:")
                    st.markdown(analysis_result)
                else:
                    st.error("An unexpected error occurred ☹️")
        except Exception as e:
            st.error(e)
    st.markdown('<span style="color: red;">NOTE: Using free-tier API keys. The token may hit its usage limit.</span>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()