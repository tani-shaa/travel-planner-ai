"""
Tab 4 — Trip Management & PDF Export
Save/load trips from SQLite, view trip history, and export to PDF.
"""

import streamlit as st
from utils.database import save_trip, get_all_trips, get_trip_by_id, delete_trip
from utils.pdf_export import generate_pdf
from utils.config import is_demo_mode
import datetime


def _format_date(iso: str) -> str:
    try:
        dt = datetime.datetime.fromisoformat(iso)
        return dt.strftime("%d %b %Y, %H:%M UTC")
    except Exception:
        return iso


def render():
    st.markdown("## 💾 Trip Manager & PDF Export")
    st.markdown("Save your itinerary, revisit past trips, and export a beautifully formatted PDF guide.")

    itinerary = st.session_state.get("itinerary")

    # ── Save Current Trip ─────────────────────────────────────────────────────
    st.markdown("### 💾 Save Current Itinerary")

    if not itinerary or not itinerary.get("days"):
        st.info("No active itinerary found. Generate one in **Tab 2** first.")
    else:
        destination = itinerary.get("destination",
            st.session_state.get("fixed_destination", "My Trip"))
        duration    = st.session_state.get("duration", len(itinerary.get("days", [])))
        budget      = st.session_state.get("budget", "Mid-Range")
        pace        = st.session_state.get("pace", "Moderate")
        travel_style = st.session_state.get("travel_style", "Solo")
        interests   = st.session_state.get("interests", [])

        with st.form("save_trip_form"):
            trip_name = st.text_input(
                "Trip name",
                value=f"{destination} — {duration} Days",
                placeholder="e.g. Summer in Lisbon",
            )
            submitted = st.form_submit_button("💾 Save Trip", type="primary", use_container_width=True)

        if submitted:
            if not trip_name.strip():
                st.warning("Please enter a name for this trip.")
            else:
                trip_id = save_trip(
                    name=trip_name.strip(),
                    destination=destination,
                    duration=duration,
                    budget=budget,
                    pace=pace,
                    travel_style=travel_style,
                    interests=interests,
                    itinerary=itinerary,
                    preferences={
                        "vibe": st.session_state.get("vibe", ""),
                        "season": st.session_state.get("season", ""),
                        "currency": st.session_state.get("currency", "USD"),
                    },
                )
                st.success(f"✅ Trip **'{trip_name}'** saved successfully! (ID: {trip_id})")

        # PDF export for active itinerary
        st.markdown("---")
        st.markdown("### 📄 Export Active Itinerary to PDF")

        pdf_name = st.text_input(
            "PDF trip name label",
            value=f"{destination} Adventure",
            key="pdf_name_active",
        )

        if st.button("📥 Download Itinerary PDF", type="primary", use_container_width=True):
            with st.spinner("Generating your PDF..."):
                pdf_bytes = generate_pdf(itinerary, trip_name=pdf_name)
            safe_name = pdf_name.replace(" ", "_").replace(",", "").replace("/", "-")
            st.download_button(
                label="⬇️ Click here to download your PDF",
                data=pdf_bytes,
                file_name=f"{safe_name}_itinerary.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
            st.success("✅ PDF ready! Click the button above to download.")

    st.markdown("---")

    # ── Trip History ──────────────────────────────────────────────────────────
    st.markdown("### 🗂️ Saved Trip History")

    trips = get_all_trips()

    if not trips:
        st.markdown("""
        <div style="text-align:center; padding:2.5rem; color:#94a3b8;">
            <div style="font-size:2.5rem;">🗃️</div>
            <p>No saved trips yet. Generate an itinerary and save it above!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"**{len(trips)} trip(s) saved**")

    for trip in trips:
        tid        = trip["id"]
        tname      = trip["name"]
        tdest      = trip["destination"]
        tdur       = trip["duration"]
        tbudget    = trip.get("budget", "")
        tpace      = trip.get("pace", "")
        tcreated   = _format_date(trip.get("created_at", ""))
        tinterests = trip.get("interests", [])

        with st.expander(f"📋 {tname}  —  {tdest}", expanded=False):
            c1, c2, c3 = st.columns(3)
            c1.metric("Destination", tdest)
            c2.metric("Duration", f"{tdur} days")
            c3.metric("Budget", tbudget)

            c4, c5, c6 = st.columns(3)
            c4.metric("Pace", tpace)
            c5.metric("Saved on", tcreated)
            c6.metric("Interests", ", ".join(tinterests[:3]) + ("…" if len(tinterests) > 3 else ""))

            btn_col1, btn_col2, btn_col3 = st.columns(3)

            with btn_col1:
                if st.button("📂 Load this trip", key=f"load_{tid}", use_container_width=True):
                    full_trip = get_trip_by_id(tid)
                    if full_trip:
                        st.session_state["itinerary"]          = full_trip["itinerary"]
                        st.session_state["fixed_destination"]  = full_trip["destination"]
                        st.session_state["duration"]           = full_trip["duration"]
                        st.session_state["budget"]             = full_trip.get("budget", "Mid-Range")
                        st.session_state["pace"]               = full_trip.get("pace", "Moderate")
                        st.session_state["travel_style"]       = full_trip.get("travel_style", "Solo")
                        st.session_state["interests"]          = full_trip.get("interests", [])
                        prefs = full_trip.get("preferences", {})
                        st.session_state["vibe"]               = prefs.get("vibe", "Beach")
                        st.session_state["season"]             = prefs.get("season", "Spring (Mar–May)")
                        st.session_state["currency"]           = prefs.get("currency", "USD")
                        st.success(f"✅ Loaded **{tname}**. Switch to Tab 2 to view it.")
                        st.rerun()

            with btn_col2:
                trip_data     = get_trip_by_id(tid)
                trip_itin     = trip_data["itinerary"] if trip_data else {}
                if trip_itin and trip_itin.get("days"):
                    pdf_bytes = generate_pdf(trip_itin, trip_name=tname)
                    safe_name = tname.replace(" ", "_").replace(",", "").replace("/", "-")
                    st.download_button(
                        label="📥 Export PDF",
                        data=pdf_bytes,
                        file_name=f"{safe_name}_itinerary.pdf",
                        mime="application/pdf",
                        key=f"pdf_{tid}",
                        use_container_width=True,
                    )

            with btn_col3:
                if st.button("🗑️ Delete", key=f"del_{tid}", use_container_width=True):
                    delete_trip(tid)
                    st.warning(f"Trip **'{tname}'** deleted.")
                    st.rerun()
