import pandas as pd


# -----------------------------
# 🔹 Helper functions
# -----------------------------

def parse_date(date_str):
    """Parse tenancy start date safely (MM/YYYY)."""
    return pd.to_datetime(date_str, format="%m/%Y", errors="coerce")


def within_floor_tolerance(row_floor, ref_floor, tolerance=0.10):
    if pd.isna(row_floor) or pd.isna(ref_floor):
        return False
    return abs(row_floor - ref_floor) <= tolerance * ref_floor


def bedrooms_within_range(row_bed, ref_bed):
    if pd.isna(row_bed):
        return False
    return abs(row_bed - ref_bed) <= 1


# -----------------------------
# 🔹 Main function
# -----------------------------

def get_comparables(csv_path, reference, lea_name):
    # Load CSV
    df = pd.read_csv(csv_path)

    # -----------------------------
    # 🔹 Data cleaning
    # -----------------------------

    # Normalize text fields
    for col in ["Dwelling Type", "BER", "Local Electoral Area"]:
        df[col] = df[col].astype(str).str.strip().str.upper()

    reference["dwelling_type"] = reference["dwelling_type"].strip().upper()
    reference["ber"] = reference["ber"].strip().upper() if reference["ber"] else ""
    lea_name = lea_name.strip().upper()

    # Numeric conversions
    df["Floor Space m2"] = pd.to_numeric(df["Floor Space m2"], errors="coerce")
    df["Number of Bedrooms"] = pd.to_numeric(df["Number of Bedrooms"], errors="coerce")

    # Optional: clean rent (not used in logic, but safe)
    if "Rent (Month)" in df.columns:
        df["Rent (Month)"] = (
            df["Rent (Month)"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    # Parse dates
    df["Tenancy Start Parsed"] = df["Tenancy Start"].apply(parse_date)

    # Drop rows with invalid dates
    df = df.dropna(subset=["Tenancy Start Parsed"])

    # Filter by Local Electoral Area
    df = df[df["Local Electoral Area"] == lea_name].copy()

    # Fill BER safely
    df["BER"] = df["BER"].fillna("")

    # -----------------------------
    # 🔹 Matching logic
    # -----------------------------

    selected_ids = set()
    results = []

    def add_matches(condition, label):
        nonlocal results, selected_ids

        subset = df[condition].copy()

        # Remove already selected rows
        subset = subset[~subset.index.isin(selected_ids)]

        # Sort by newest tenancy
        subset = subset.sort_values(
            by="Tenancy Start Parsed", ascending=False
        )

        for idx, row in subset.iterrows():
            if len(results) >= 10:
                break

            row_out = row.copy()
            row_out["Match Category"] = label

            results.append(row_out)
            selected_ids.add(idx)

    # -----------------------------
    # 🔹 Level 0 — Exact
    # -----------------------------
    add_matches(
        (df["Dwelling Type"] == reference["dwelling_type"]) &
        (df["Number of Bedrooms"] == reference["bedrooms"]) &
        (df["BER"] == reference["ber"]) &
        (df["Floor Space m2"].apply(
            lambda x: within_floor_tolerance(x, reference["floor_space"])
        )),
        "Exact"
    )

    # -----------------------------
    # 🔹 Level 1 — BER relaxed
    # -----------------------------
    if len(results) < 10:
        add_matches(
            (df["Dwelling Type"] == reference["dwelling_type"]) &
            (df["Number of Bedrooms"] == reference["bedrooms"]) &
            (df["Floor Space m2"].apply(
                lambda x: within_floor_tolerance(x, reference["floor_space"])
            )),
            "BER relaxed"
        )

    # -----------------------------
    # 🔹 Level 2 — Floor relaxed
    # -----------------------------
    if len(results) < 10:
        add_matches(
            (df["Dwelling Type"] == reference["dwelling_type"]) &
            (df["Number of Bedrooms"] == reference["bedrooms"]),
            "Floor relaxed"
        )

    # -----------------------------
    # 🔹 Level 3 — Bedrooms ±1
    # -----------------------------
    if len(results) < 10:
        add_matches(
            (df["Dwelling Type"] == reference["dwelling_type"]) &
            (df["Number of Bedrooms"].apply(
                lambda x: bedrooms_within_range(x, reference["bedrooms"])
            )),
            "Bedroom relaxed"
        )

    # -----------------------------
    # 🔹 Final output
    # -----------------------------

    if results:
        final_df = pd.DataFrame(results)
    else:
        final_df = pd.DataFrame()

    return final_df


# -----------------------------
# 🔹 Example usage
# -----------------------------

if __name__ == "__main__":
    import sys
    import importlib.util
    import os

    # -----------------------------
    # 🔹 Get parameter file from CLI
    # -----------------------------
    if len(sys.argv) < 2:
        print("Usage: python script.py <params_file.py>")
        sys.exit(1)

    params_path = sys.argv[1]

    # -----------------------------
    # 🔹 Dynamically load params file
    # -----------------------------
    spec = importlib.util.spec_from_file_location("params", params_path)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    # -----------------------------
    # 🔹 Build reference object
    # -----------------------------
    reference = {
        "eircode": getattr(params, "reference_eircode", None),
        "dwelling_type": params.reference_dwelling_type,
        "ber": params.reference_ber,
        "bedrooms": params.reference_bedrooms,
        "floor_space": params.reference_floor_space
    }

    lea_name = params.lea_name

    # -----------------------------
    # 🔹 Run matching
    # -----------------------------
    output = get_comparables(
        csv_path=params.dataset,
        reference=reference,
        lea_name=lea_name
    )

    print(output)

    # -----------------------------
    # 🔹 Output filename (uses LEA)
    # -----------------------------
    safe_lea = lea_name.replace(" ", "_")

    output_file = f"comparables_{safe_lea}.csv"
    output.to_csv(output_file, index=False)

    print(f"\nSaved to: {output_file}")