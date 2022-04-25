##  A real life ecommerce payment workflow problem

### Problem Statement

An e-commerce owner has 6 category of items to sell (limited available quantity)
- T-shirt with Yellowstone logo $19.99 / each (20 available);
- T-shirt with Big Teton logo $19.99 / each (20 available);
- T-shirt with Glacier logo $19.99 / each (20 available);

- Jacket with Yellowstone logo $49.99 / each (30 available);
- Jacket with Big Teton logo $49.99 / each (30 available);
- Jacket with Glacier logo $49.99 / each (30 available);

She wanted to build a checkout system allowing her customer to select items and checkout, so that
- The customer fills his/her personal info (i.e., name, phone number, email...) and select the wanted items;
- when checking out, after the customer inputs credit card and proceeds, the system charges the credit card;
- if the charge succeeds, the system fills the customer info into the database of "to be shipped items", and let the customer know everything worked;
- if the charge does not succeed, the system fill the customer info into the database of "unsuccessful charges", and let the customer know charge did not happen;

### Hint
1. How to simplify the front-end building process (listing the available items and their price, collect customer info...)? (will a Google Form work for a simple prototype?)
2. How to simplify the databases building process? (will a Google Spreadsheet work for a simple prototype?)
3. How to handle credit card charging process? (will a Stripe API work?)
4. How to handle the successful charging and unsuccessful charging, a simple state machine? (Do you happen to know AWS StepFunction?)

If you happen to follow this hint, you have already ended up buiding a Zapier backend on your own, congratulations! Happy hacking.

