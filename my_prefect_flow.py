from prefect import flow, task

# Define a simple task
@task
def say_hello(name: str):
    print(f"Hello, {name}!")

# Define a flow
@flow
def my_first_flow():
    say_hello("World")

# Run the flow
if __name__ == "__main__":
    my_first_flow()
