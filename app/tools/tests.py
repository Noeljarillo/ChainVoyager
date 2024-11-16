from  get_yields import fetch_and_save_pools_data
from find_optimal import get_optimal_pools


def test_fetch_and_save_pools_data():

    db_path = "../../db/pools_data.db"
    
    try:
        fetch_and_save_pools_data(db_path)
        print("Test passed: Data fetched and saved successfully.")
    except Exception as e:
        print(f"Test failed: {e}")

# Run the test
test_fetch_and_save_pools_data()



top_pools = get_optimal_pools(
    db_path='../../db/pools_data.db',
    exposure='single',
    stablecoin=True,  
    chain='Ethereum',
    top_n=5
)


print(top_pools)
