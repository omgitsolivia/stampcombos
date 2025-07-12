# Copyright (C) 2025 Olivia Godwin
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# <https://mozilla.org/MPL/2.0/>.
#
# SPDX-License-Identifier: MPL-2.0


import itertools

import streamlit as st


def calculate_stamp_combos(
    price_dollars: float,
    stamps: list[int],
    max_stamps: int = 5,
    max_price_dollars: float = 1.74,
):
    """Calculate valid stamp combinations given constraints."""
    price_cents = int(price_dollars * 100)
    max_price_cents = int(max_price_dollars * 100)
    combos = itertools.chain(
        *(
            itertools.combinations_with_replacement(stamps, n)
            for n in range(1, max_stamps + 1)
        )
    )
    return [
        combo
        for combo in combos
        if (sum(combo) >= price_cents and sum(combo) <= max_price_cents)
    ]


def main():
    st.title("📮 Postage Stamp Calculator")
    st.markdown(
        """Find all possible combinations of stamps that add up to your target postage
    amount. This calculator helps you determine the exact stamps needed for mailing,
    ensuring you don't exceed your maximum price limit while using the fewest stamps
    possible."""
    )

    # Create input sections
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✉️ Available Stamp Denominations")
        stamps_input = st.text_input(
            "Enter stamp values in cents (comma-separated)",
            placeholder="78, 44, 37, 29, 25, 20",
            help=(
                "Enter the cent values of your available stamps, separated by commas "
                "(e.g., 78, 44, 37)"
            )
        )

        # Parse stamps
        if stamps_input:
            try:
                stamps = [int(x.strip()) for x in stamps_input.split(',') if x.strip()]
                if stamps:
                    stamp_display = [f"{s}¢" for s in sorted(stamps, reverse=True)]
                    st.success(
                        f"Loaded {len(stamps)} stamp denominations: "
                        f"{', '.join(stamp_display)}"
                    )
                else:
                    st.error("Please enter at least one stamp value")
            except ValueError:
                st.error("Please enter valid numbers separated by commas")
        else:
            st.info("Please enter your available stamp denominations above")

    with col2:
        st.subheader("💰 Postage Requirements")
        price = st.number_input(
            "Target postage amount ($)",
            min_value=0.01,
            value=None,
            step=0.01,
            format="%.2f",
            placeholder="1.70",
            help="The exact postage amount you need to reach in dollars"
        )

        max_price = st.number_input(
            "Maximum price ($)",
            min_value=price if price else 0.01,
            value=None,
            step=0.01,
            format="%.2f",
            placeholder="1.74",
            help="Maximum total amount you're willing to pay (must not be exceeded)"
        )

        max_stamps = st.number_input(
            "Maximum number of stamps",
            min_value=1,
            max_value=10,
            value=None,
            placeholder="5",
            help="Limit the total number of stamps used in any combination"
        )

    # Calculate combinations button
    if st.button("🔍 Calculate Stamp Combinations", type="primary"):
        # Validate all inputs are provided
        if not stamps_input:
            st.error("Please enter stamp denominations")
            return
        if price is None:
            st.error("Please enter a target postage amount")
            return
        if max_price is None:
            st.error("Please enter a maximum price")
            return
        if max_stamps is None:
            st.error("Please enter a maximum number of stamps")
            return
            
        with st.spinner("Finding all possible stamp combinations..."):
            try:
                valid_combos = calculate_stamp_combos(
                    price, stamps, max_stamps, max_price
                )

                if valid_combos:
                    st.success(f"Found {len(valid_combos)} valid stamp combinations!")

                    # Display results
                    st.subheader(f"💰 Stamp Combinations for ${price:.2f} Postage")

                    # Create a table for better visualization
                    results_data = []
                    for combo in valid_combos:
                        total_cents = sum(combo)
                        total_dollars = total_cents / 100
                        stamps_used = len(combo)
                        overpayment_cents = total_cents - int(price * 100)
                        overpayment_dollars = overpayment_cents / 100
                        combo_str = " + ".join([str(s) for s in combo])
                        results_data.append({
                            "Stamp Combination (¢)": combo_str,
                            "Total Cost": f"${total_dollars:.2f}",
                            "Number of Stamps": stamps_used,
                            "Overpayment": f"${overpayment_dollars:.2f}"
                        })

                    # Sort by total cost (ascending)
                    results_data.sort(key=lambda x: float(x["Total Cost"][1:]))

                    # Display as dataframe
                    st.dataframe(
                        results_data,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Summary statistics
                    st.subheader("📊 Summary")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Total Combinations", len(valid_combos))

                    with col2:
                        min_total_cents = min(sum(combo) for combo in valid_combos)
                        min_total_dollars = min_total_cents / 100
                        st.metric("Minimum Cost", f"${min_total_dollars:.2f}")

                    with col3:
                        max_total_cents = max(sum(combo) for combo in valid_combos)
                        max_total_dollars = max_total_cents / 100
                        st.metric("Maximum Cost", f"${max_total_dollars:.2f}")

                    with col4:
                        min_stamps = min(len(combo) for combo in valid_combos)
                        st.metric("Fewest Stamps", min_stamps)

                    # Best options
                    st.subheader("🌟 Recommended Combinations")

                    # Find combination with minimum overpayment
                    price_cents = int(price * 100)
                    min_overpay_combo = min(
                        valid_combos, key=lambda x: sum(x) - price_cents
                    )
                    min_overpay_cents = sum(min_overpay_combo) - price_cents
                    min_overpay_dollars = min_overpay_cents / 100

                    # Find combination with fewest stamps
                    min_stamps_combo = min(valid_combos, key=len)

                    col1, col2 = st.columns(2)

                    with col1:
                        combo_display = ' + '.join([f"{s}¢" for s in min_overpay_combo])
                        total_min_overpay_dollars = sum(min_overpay_combo) / 100
                        st.info(
                            f"**Lowest Overpayment:** {combo_display}\n\n"
                            f"Total: ${total_min_overpay_dollars:.2f} "
                            f"(overpay: ${min_overpay_dollars:.2f})"
                        )

                    with col2:
                        combo_display = ' + '.join([f"{s}¢" for s in min_stamps_combo])
                        total_min_stamps_dollars = sum(min_stamps_combo) / 100
                        st.info(
                            f"**Fewest Stamps:** {combo_display}\n\n"
                            f"Total: ${total_min_stamps_dollars:.2f} "
                            f"({len(min_stamps_combo)} stamps)"
                        )

                else:
                    st.warning(
                        "No valid stamp combinations found with these parameters."
                    )
                    st.info(
                        "Try increasing the maximum price limit or the maximum number "
                        "stamps allowed."
                    )

            except ValueError as e:
                st.error(f"An error occurred: {e!s}")

    # Instructions
    with st.expander("ℹ️ How to Use This Calculator"):  # noqa: RUF001
        st.markdown(
            """
        **Step-by-step guide:**

        1. **Enter available stamp denominations** - List the cent values of stamps
           you have
           available (comma-separated)
        2. **Set target postage amount** - Enter the exact postage amount needed in
           dollars
        3. **Set maximum price** - Enter the maximum total amount you're willing to pay
           (cannot be exceeded)
        4. **Set stamp limit** - Choose the maximum number of stamps to use in any
           combination
        5. **Calculate combinations** - Click the button to find all possible stamp
           combinations

        **Results include:**
        - All valid stamp combinations sorted by total cost
        - Summary statistics showing cost ranges and stamp counts
        - Recommended options for lowest overpayment and fewest stamps

        **Example:** For $1.70 postage with stamps worth 78¢, 44¢, 37¢, 29¢, 25¢, 20¢
        """
        )


if __name__ == "__main__":
    main()
