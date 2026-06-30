#!/usr/bin/env zsh
# Rename raw Barchart/Koyfin downloads → canonical staged filename contract.
# Authority: Master Data Dictionary v1.0 (whinfell_pipeline/data_dictionary.yaml)
# Usage: scripts/normalize_whinfell_drop.sh [drop_dir]
# Default drop_dir: ~/Downloads/whinfell_drop
set -euo pipefail

DROP="${1:-$HOME/Downloads/whinfell_drop}"
STAMP_DEFAULT="20260628"

if [[ ! -d "$DROP" ]]; then
  echo "ERROR: drop dir not found: $DROP" >&2
  exit 1
fi

# HHMM from file mtime (local), YYYYMMDD from filename or mtime.
file_hhmm() {
  local f="$1"
  date -r "$f" "+%H%M" 2>/dev/null || stat -f "%Sm" -t "%H%M" "$f"
}

file_yyyymmdd() {
  local f="$1"
  local base="${f:t:r}"
  if [[ "$base" =~ ([0-9]{2})-([0-9]{2})-([0-9]{4}) ]]; then
    echo "${match[3]}${match[1]}${match[2]}"
    return 0
  fi
  if [[ "$base" =~ ([0-9]{4})-([0-9]{2})-([0-9]{2}) ]]; then
    echo "${match[1]}${match[2]}${match[3]}"
    return 0
  fi
  date -r "$f" "+%Y%m%d" 2>/dev/null || stat -f "%Sm" -t "%Y%m%d" "$f"
}

rename_one() {
  local src="$1" dest_name="$2"
  local dest="$DROP/$dest_name"
  if [[ "$src" == "$dest" ]]; then
    echo "skip  already canonical: $dest_name"
    return 0
  fi
  if [[ -e "$dest" ]]; then
    echo "skip  target exists: $dest_name  (source: ${src:t})"
    return 0
  fi
  mv "$src" "$dest"
  echo "ok    ${src:t}  ->  $dest_name"
}

echo "=== normalize_whinfell_drop ==="
echo "drop=$DROP"
echo ""

RENAMED=0
SKIPPED=0

for f in "$DROP"/*.csv(N); do
  base="${f:t}"
  # Skip duplicates / noise.
  if [[ "$base" == *" (1).csv" ]]; then
    echo "skip  duplicate copy: $base"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  ymd="$(file_yyyymmdd "$f")"
  hhmm="$(file_hhmm "$f")"
  [[ -n "$ymd" ]] || ymd="$STAMP_DEFAULT"

  case "$base" in
    btm26_daily-nearby_historical-data-*)
      rename_one "$f" "futures_daily_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    btn26-options-monthly-options-exp-*side-by-side-intraday*)
      rename_one "$f" "options_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    btn26-volatility-greeks-exp-*)
      rename_one "$f" "greeks_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    futures-spreads-btn26-*)
      rename_one "$f" "btc_basis_${ymd}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    koyfin_????-??-??-?.csv|koyfin_????-??-??-??.csv)
      rename_one "$f" "crypto_corr_series_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    koyfin_2026-06-28.csv|koyfin_????-??-??.csv)
      rename_one "$f" "rates_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    *crypto-price*|*Crypto-Price*|*WTM-Crypto-Price*)
      rename_one "$f" "btc_price_chart_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    *crypto-correl*btc*|*Crypto-Correl*BTC*|*WTM-Crypto-Correl*BTC*)
      rename_one "$f" "btc_correl_chart_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    *crypto-correl*eth*|*Crypto-Correl*ETH*)
      rename_one "$f" "eth_correl_chart_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    *crypto-correl*xrp*|*Crypto-Correl*XRP*)
      rename_one "$f" "xrp_correl_chart_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    *crypto-correl*sol*|*Crypto-Correl*SOL*)
      rename_one "$f" "sol_correl_chart_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    *WTM-Crypto-Correl*)
      rename_one "$f" "btc_correl_chart_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    koyfin_Simplify_All_ETFs_*)
      rename_one "$f" "equities_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    koyfin_WhinPump*)
      rename_one "$f" "credit_${ymd}_${hhmm}.csv" && RENAMED=$((RENAMED + 1))
      ;;
    futures_intraday_*|futures_daily_*|options_*|greeks_*|btc_basis_*|rates_*|credit_*|equities_*|china_policy_*|crypto_*|btc_price_chart_*|btc_correl_chart_*|eth_correl_chart_*|xrp_correl_chart_*|sol_correl_chart_*)
      echo "skip  already canonical: $base"
      SKIPPED=$((SKIPPED + 1))
      ;;
    *)
      echo "warn  no rule for: $base"
      SKIPPED=$((SKIPPED + 1))
      ;;
  esac
done

echo ""
echo "done  renamed=$RENAMED skipped=$SKIPPED"
echo ""
echo "Next:"
echo "  cd ~/Desktop/Whinfell_BUILD_Cousins"
echo "  python3 run_csv_download.py stage --downloads $DROP --operator desk --window today"
echo ""
echo "NOTE: Raw Barchart/Koyfin column layouts still fail header validation."
echo "      Staged CSVs need WTM observation rows (see whinfell_pipeline/examples/staged/)."
echo "      Use Transmission Control WTM EXPORT or Comet collector shaped exports for ingest."