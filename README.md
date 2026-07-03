## Telegram Clock Bio

This script updates your Telegram profile information (bio and/or name) at regular intervals and displays the current time based on your selected timezone. It supports configurable update modes, safe rate-limited updates, and optional emoji-based clock indicators.



## Installation

Install required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```



## Configuration

All settings are managed through `config.json`.

Example configuration:

```json
{
  "api_id": 123456,
  "api_hash": "YOUR_API_HASH",
  "timezone": "America/New_York",

  "update_mode": "both",
  "interval": 60,

  "bio_template": "You will see this at {time} {emoji}",
  "name_template": "{emoji} {time}",

  "use_emoji": true,
  "safe_mode": true
}
```

### Configuration options

* `update_mode`

  * `bio` → only updates bio
  * `name` → only updates name
  * `both` → updates both

* `interval`

  * Time in seconds between updates

* `bio_template`

  * Template for Telegram bio

* `name_template`

  * Template for Telegram first name

* `use_emoji`

  * Enables or disables clock emoji

* `safe_mode`

  * Adds slight randomness to prevent strict update patterns



## Execution

Run the script using:

```bash
python main.py
```



## Stopping Execution

To stop the script, press:

```
Ctrl + C
```



## Notes

* Telegram API credentials must be valid and correctly set in `config.json`.
* Frequent profile updates may cause temporary restrictions from Telegram if abused.
* Safe mode is enabled by default to reduce the risk of rate limiting.
* The script automatically skips updates if no changes are detected.



## Warning

This script interacts with Telegram’s official API and modifies user profile data. Improper or excessive usage may violate Telegram’s terms of service and can lead to temporary limitations on your account. Use responsibly.
