import requests
import gradio as gr
from datetime import datetime


CURRENCIES = [
    "USD", "LKR", "EUR", "GBP", "AED", "AUD", "CAD",
    "CHF", "CNY", "HKD", "INR", "JPY", "KRW", "KWD",
    "MYR", "NZD", "QAR", "SAR", "SGD", "THB"
]


def get_live_rates(base_currency):
    """Retrieve the latest exchange rates."""

    url = (
        f"https://open.er-api.com/v6/latest/"
        f"{base_currency.upper()}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        if data.get("result") == "success":
            return data.get("rates", {}), data.get("time_last_update_utc")

        return None, None

    except requests.RequestException:
        return None, None


def convert_currency(amount, from_currency, to_currency):
    """Convert an amount between two currencies."""

    if amount is None:
        return (
            """
            <div class="result-card error-card">
                <div class="result-icon">⚠️</div>
                <h3>Amount required</h3>
                <p>Please enter an amount to convert.</p>
            </div>
            """,
            ""
        )

    if amount < 0:
        return (
            """
            <div class="result-card error-card">
                <div class="result-icon">⚠️</div>
                <h3>Invalid amount</h3>
                <p>Please enter an amount greater than or equal to zero.</p>
            </div>
            """,
            ""
        )

    if not from_currency or not to_currency:
        return (
            """
            <div class="result-card error-card">
                <div class="result-icon">⚠️</div>
                <h3>Select currencies</h3>
                <p>Please select both the base and target currencies.</p>
            </div>
            """,
            ""
        )

    rates, last_updated = get_live_rates(from_currency)

    if not rates:
        return (
            """
            <div class="result-card error-card">
                <div class="result-icon">📡</div>
                <h3>Connection error</h3>
                <p>Unable to retrieve the latest exchange rates.</p>
            </div>
            """,
            ""
        )

    if to_currency not in rates:
        return (
            f"""
            <div class="result-card error-card">
                <div class="result-icon">❌</div>
                <h3>Unsupported currency</h3>
                <p>No exchange rate is available for {to_currency}.</p>
            </div>
            """,
            ""
        )

    rate = rates[to_currency]
    converted_amount = amount * rate

    result = f"""
    <div class="result-card success-card">
        <div class="result-icon">💰</div>

        <div class="conversion-label">Converted Amount</div>

        <div class="converted-amount">
            {converted_amount:,.2f}
            <span>{to_currency}</span>
        </div>

        <div class="original-amount">
            {amount:,.2f} {from_currency}
        </div>

        <div class="rate-line">
            1 {from_currency} = {rate:,.6f} {to_currency}
        </div>
    </div>
    """

    update_information = f"""
    <div class="update-information">
        <span>🕒 Rate updated:</span>
        <strong>{last_updated or "Latest available rate"}</strong>
    </div>
    """

    return result, update_information


def swap_currencies(from_currency, to_currency):
    """Swap the selected currencies."""

    return to_currency, from_currency


def reset_converter():
    """Restore the default values."""

    return (
        1,
        "USD",
        "LKR",
        """
        <div class="result-card welcome-card">
            <div class="result-icon">🌍</div>
            <h3>Ready to convert</h3>
            <p>Enter an amount and select your currencies.</p>
        </div>
        """,
        ""
    )


custom_css = """
.gradio-container {
    max-width: 820px !important;
    margin: auto !important;
    font-family: Inter, Arial, sans-serif !important;
}

.hero {
    padding: 32px 20px 20px;
    text-align: center;
}

.hero-icon {
    width: 82px;
    height: 82px;
    display: flex;
    margin: auto;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    color: white;
    font-size: 42px;
    background: linear-gradient(135deg, #059669, #0284c7);
    box-shadow: 0 15px 35px rgba(5, 150, 105, 0.28);
}

.hero h1 {
    margin: 18px 0 6px;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero p {
    margin: 0;
    color: #64748b;
    font-size: 16px;
}

.converter-box {
    padding: 8px !important;
    border-radius: 24px !important;
}

#amount-input input {
    font-size: 23px !important;
    font-weight: 700 !important;
}

#convert-button {
    min-height: 48px !important;
    color: white !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    background: linear-gradient(
        135deg,
        #059669,
        #0284c7
    ) !important;
}

#swap-button {
    min-width: 55px !important;
    max-width: 55px !important;
    margin-top: 27px !important;
    font-size: 20px !important;
}

.result-card {
    padding: 28px 20px;
    margin-top: 18px;
    border: 1px solid transparent;
    border-radius: 22px;
    text-align: center;
}

.result-icon {
    margin-bottom: 8px;
    font-size: 38px;
}

.welcome-card {
    color: #334155;
    border-color: #cbd5e1;
    background: #f8fafc;
}

.welcome-card h3,
.error-card h3 {
    margin: 5px 0;
}

.welcome-card p,
.error-card p {
    margin: 0;
}

.success-card {
    color: #064e3b;
    border-color: #a7f3d0;
    background: linear-gradient(135deg, #ecfdf5, #eff6ff);
    box-shadow: 0 12px 30px rgba(5, 150, 105, 0.12);
}

.error-card {
    color: #991b1b;
    border-color: #fecaca;
    background: #fef2f2;
}

.conversion-label {
    margin-bottom: 5px;
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.converted-amount {
    margin: 5px 0;
    font-size: 39px;
    font-weight: 800;
    letter-spacing: -1px;
}

.converted-amount span {
    font-size: 20px;
    font-weight: 700;
}

.original-amount {
    color: #475569;
    font-size: 16px;
}

.rate-line {
    display: inline-block;
    margin-top: 18px;
    padding: 9px 15px;
    border-radius: 20px;
    color: #0369a1;
    background: rgba(224, 242, 254, 0.8);
    font-size: 14px;
    font-weight: 700;
}

.update-information {
    margin-top: 10px;
    color: #64748b;
    text-align: center;
    font-size: 12px;
}

.footer {
    margin-top: 22px;
    color: #94a3b8;
    text-align: center;
    font-size: 12px;
}

@media (max-width: 600px) {
    .hero h1 {
        font-size: 28px;
    }

    .converted-amount {
        font-size: 31px;
    }

    #swap-button {
        margin-top: 0 !important;
        max-width: none !important;
    }
}
"""


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="emerald",
        secondary_hue="sky",
        radius_size="lg"
    ),
    css=custom_css,
    title="Live Currency Converter"
) as app:

    gr.HTML("""
    <div class="hero">
        <div class="hero-icon">💱</div>
        <h1>Currency Converter</h1>
        <p>Convert currencies using the latest available rates.</p>
    </div>
    """)

    with gr.Group(elem_classes="converter-box"):

        amount_input = gr.Number(
            value=1,
            label="Amount",
            minimum=0,
            elem_id="amount-input"
        )

        with gr.Row():
            from_currency = gr.Dropdown(
                choices=CURRENCIES,
                value="USD",
                label="From",
                scale=5
            )

            swap_button = gr.Button(
                "⇄",
                elem_id="swap-button",
                scale=1
            )

            to_currency = gr.Dropdown(
                choices=CURRENCIES,
                value="LKR",
                label="To",
                scale=5
            )

        with gr.Row():
            reset_button = gr.Button("Reset")

            convert_button = gr.Button(
                "Convert Currency →",
                variant="primary",
                elem_id="convert-button"
            )

        result_output = gr.HTML("""
        <div class="result-card welcome-card">
            <div class="result-icon">🌍</div>
            <h3>Ready to convert</h3>
            <p>Enter an amount and select your currencies.</p>
        </div>
        """)

        update_output = gr.HTML()

    gr.HTML("""
    <div class="footer">
        Exchange rates are indicative and may differ from bank rates.
    </div>
    """)

    convert_button.click(
        fn=convert_currency,
        inputs=[
            amount_input,
            from_currency,
            to_currency
        ],
        outputs=[
            result_output,
            update_output
        ]
    )

    amount_input.submit(
        fn=convert_currency,
        inputs=[
            amount_input,
            from_currency,
            to_currency
        ],
        outputs=[
            result_output,
            update_output
        ]
    )

    swap_button.click(
        fn=swap_currencies,
        inputs=[
            from_currency,
            to_currency
        ],
        outputs=[
            from_currency,
            to_currency
        ]
    ).then(
        fn=convert_currency,
        inputs=[
            amount_input,
            from_currency,
            to_currency
        ],
        outputs=[
            result_output,
            update_output
        ]
    )

    reset_button.click(
        fn=reset_converter,
        outputs=[
            amount_input,
            from_currency,
            to_currency,
            result_output,
            update_output
        ]
    )


app.launch(share=True, debug=True)
