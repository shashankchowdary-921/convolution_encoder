import streamlit as st

def render_transmission_section(
    input_text,
    recovered_text,
    ber,
    errors_introduced,
    errors_corrected,
    recovery_efficiency
):

    st.subheader("Transmission Result")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Input Message")
        st.write(input_text)

    with col2:
        st.write("Recovered Message")
        st.write(recovered_text)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("BER", f"{ber:.6f}")

    with c2:
        st.metric("Errors Introduced", errors_introduced)

    with c3:
        st.metric("Errors Corrected", errors_corrected)

    with c4:
        st.metric(
            "Recovery Efficiency",
            f"{recovery_efficiency:.1f}%"
        )
