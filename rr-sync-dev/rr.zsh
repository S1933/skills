rr() {
  local PROJECT="${1:-ocms}"
  local REMOTE_HOST="gw2sdev-docker.ovh.net"
  local REMOTE_ROOT="/home/jnuel/sshfs/$PROJECT"
  local files=()

  shift 2>/dev/null || true

  if [ "$#" -gt 0 ]; then
    files=("$@")
  else
    echo "📦 No files args → using git status..."
    echo "📁 Project: $PROJECT"

    while IFS= read -r line; do
      file="${line:3}"
      files+=("$file")
    done < <(git status --porcelain)

    if [ "${#files[@]}" -eq 0 ]; then
      echo "✅ Nothing to sync"
      return
    fi
  fi

  echo "📋 Files to sync to $PROJECT:"
  for f in "${files[@]}"; do
    echo " - $f"
  done

  echo ""
  read "confirm?🚀 Proceed with rsync to $PROJECT? (y/N): "

  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "❌ Cancelled"
    return
  fi

  for f in "${files[@]}"; do
    if [ ! -e "$f" ]; then
      echo "⚠️ Missing: $f"
      continue
    fi

    if [ -d "$f" ]; then
      rsync -avz "${f%/}/" "$REMOTE_HOST:$REMOTE_ROOT/$f"
    else
      rsync -avz "$f" "$REMOTE_HOST:$REMOTE_ROOT/$f"
    fi
  done

  echo "✅ Done"
}
