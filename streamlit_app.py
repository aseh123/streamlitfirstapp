import streamlit as st
import requests
import math

def round(value, decimals):
    return round(value, decimals)

st.title("Maya Liquidity Auction ILP Calculator")

st.markdown("""
The calculator currently caters to Rune tier 1 users and assumes that no funds are added or withdrawn from the LP. Additionally, it does not account for earned fees, resulting in an APY of 0. The calculator utilizes a constant product formula.

#### Features
1. This calculator provides information regarding Rune and Cacao assets added at the beginning of the LA lockup period.
2. It offers details on actual Rune assets and profits gained with added assets.
3. Additionally, if the user provides predicted values and the number of days for withdrawal, the calculator can compute Impermanent Loss.
4. The calculator uses initial prices from shared charts in Discord and initial quantity values from the mayanode.explorer.
5. The final quantities of Cacao and Rune are calculated using a constant product formula while considering the lockup period and a 50-day clip off.
6. Furthermore, the calculator adjusts the ILP coverage percentage by adding 100 days or 400 days, based on the Rune/Cacao ratio's over-performance or under-performance.
7. It provides ILP coverage in CACAO and hold vs. performance numbers, as well as added asset performance vs. holding a single asset added to LA.
8. Finally, the calculator outputs the final values of Rune and Cacao after the ILP coverage.
""")

maya_address = st.text_input("Enter your Maya Address:")

if maya_address:
    if not maya_address.lower().startswith('maya') or len(maya_address) != 43:
        st.error("Not a valid Maya Address")
    else:
        link = f'https://mayanode.mayachain.info/mayachain/liquidity_auction_tier/thor.rune/{maya_address}'
        response = requests.get(link)

        if response.status_code == 404:
            st.error("Not a valid Maya Address")
        elif response.ok:
            data = response.json()
            liquidity_provider = data['liquidity_provider']
            cacaofull = float(liquidity_provider['cacao_deposit_value']) / 1e10
            runefull = float(liquidity_provider['asset_deposit_value']) / 1e8
            total_asset_value = cacaofull * 0.14173 + runefull * 1.65

            st.markdown(f"#### Your assets at the start of LA:")
            st.markdown(f"Num of $RUNE: {round(runefull, 2)}")
            st.markdown(f"Num of $CACAO: {round(cacaofull, 2)}")
            st.markdown(f"Total value of assets: ${round(total_asset_value, 2)}")

            tier = data['tier']
            if tier == 1:
                rune_before_la = runefull / 1.019765
                profit_before_la = total_asset_value - rune_before_la * 1.65

                st.markdown(f"Num of $RUNE you added in LA: {round(rune_before_la, 2)}")
                st.markdown(f"Your profit at the start of LA is ${round(profit_before_la, 2)}")

                pred_rune = st.number_input("Predicted $RUNE Value:", value=3.00, min_value=0.0, step=0.01)
	        pred_cacao = st.number_input("Predicted $CACAO Value:", value=0.14173, min_value=0.0, step=0.00001)
		pred_apy = st.number_input("Predicted number of days to withdraw:", value=50, min_value=50, step=1)
	        if pred_rune and pred_cacao and pred_apy:
                        K = runefull * cacaofull
                        rt = pred_rune / pred_cacao
                        qp_rune = math.sqrt(K / rt)
                        qp_cacao = math.sqrt(K * rt)
                        p_value = qp_rune * pred_rune + qp_cacao * pred_cacao
                        hold_total_asset_value = pred_rune * runefull + pred_cacao * cacaofull
                        i_loss = p_value - hold_total_asset_value
                        i_loss_percent = (hold_total_asset_value - p_value) * 100 / hold_total_asset_value
                        init_ratio = 1.65 / 0.14173
                        pred_ratio = pred_rune / pred_cacao
        
                        st.markdown(f"#### If you withdraw at the {pred_apy} day")
                        st.markdown(f"Num of $RUNE: {round(qp_rune, 2)}")
                        st.markdown(f"Num of $CACAO: {round(qp_cacao, 2)}")
                        st.markdown(f"Your value of assets in ($): {round(p_value, 2)}")
                        st.markdown(f"Impermanent Loss (IL) percentage: {round(i_loss_percent, 2)}")
                        st.markdown(f"Performance vs HODL in ($): {round(-(hold_total_asset_value - p_value), 2)}")
                        st.markdown(f"Performance vs added asset in LA in ($): {round(p_value - 1.65 * runefull, 2)} Free Money")
        
                        if pred_ratio < init_ratio and i_loss < 0:
                            if pred_apy > 450:
                                pred_days = 450
                            else:
                                pred_days = pred_apy
                            days_covered = (pred_days - 50)
                            ILP_covered = -i_loss * days_covered / 400
        
                            st.markdown("This is $cacao overperformance case, considers 400 days for full ILP")
                            st.markdown(f"ILP covered in ($): {round(ILP_covered, 2)}")
                            IlP_percent = -ILP_covered * 100 / i_loss
                            st.markdown(f"ILP covered in percentage: {round(IlP_percent, 2)}")
                            cacao_ILP = ILP_covered / pred_cacao
                            st.markdown(f"ILP is Paid via $cacao: {round(cacao_ILP, 2)}")
                            st.markdown(f"After ILP covered, You will have {round(qp_rune, 2)} Rune")
                            total_cacao = qp_cacao + cacao_ILP
                            st.markdown(f"After ILP covered, You will have {round(total_cacao, 2)} Cacao")
                            st.markdown("Note: All these are based on assumptions, such as no withdrawal/deposit of funds from the LP position, and do not consider earned fees. This is still a work in progress - Beta Stage.")
        
                        elif pred_ratio >= init_ratio and i_loss < 0:
                            if pred_apy > 150:
                                pred_days = 150
                            else:
                            pred_days = pred_apy
                            days_covered = (pred_days - 50)
                            ILP_covered = -i_loss * days_covered / 100
                            st.markdown("This is $rune overperformance case, considers 100 days for full ILP")
                            st.markdown(f"ILP covered in ($): {round(ILP_covered, 2)}")
                            IlP_percent = -ILP_covered * 100 / i_loss
                            st.markdown(f"ILP covered in percentage: {round(IlP_percent, 2)}")
                            cacao_ILP = ILP_covered / pred_cacao
                            st.markdown(f"ILP is Paid via $cacao: {round(cacao_ILP, 2)}")
                            st.markdown(f"After ILP covered, You will have {round(qp_rune, 2)} Rune")
                            total_cacao = qp_cacao + cacao_ILP
                            st.markdown(f"After ILP covered, You will have {round(total_cacao, 2)} Cacao")
                            st.markdown("Note: All these are based on assumptions, such as no withdrawal/deposit of funds from the LP position, and do not consider earned fees. This is still a work in progress - Beta Stage.")
                        else:
                        st.markdown("No ILP coverage is needed in this scenario.")
                        st.markdown("Note: All these are based on assumptions, such as no withdrawal/deposit of funds from the LP position, and do not consider earned fees. This is still a work in progress - Beta Stage.")

