#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Policy file (assumed to be in the same directory as the script)
POLICY_FILE="$SCRIPT_DIR/pin2_user_policy.json"

# Check if the policy file exists
if [[ ! -f "$POLICY_FILE" ]]; then
    echo "Error: The policy file '$POLICY_FILE' does not exist."
    exit 1
fi

# User and policy names
USER_NAME="pin2_user"
POLICY_NAME="pin2_user_policy"

# Execute the command to update the policy
aws iam put-user-policy --user-name "$USER_NAME" --policy-name "$POLICY_NAME" --policy-document "file://$POLICY_FILE"

# Check if the command was successful
if [[ $? -eq 0 ]]; then
    echo "Policy successfully applied for user '$USER_NAME'."
else
    echo "Failed to apply the policy. Check AWS CLI permissions and configuration."
    exit 2
fi

echo "Policy applied successfully for user '$USER_NAME'."