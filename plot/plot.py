import matplotlib.pyplot as plt

def plot_head_shoulder(df):
    # Plot the High and Low prices
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['High'], label='High', color='blue', alpha=0.7)
    plt.plot(df['date'], df['Low'], label='Low', color='orange', alpha=0.7)

    # Highlight the Head and Shoulder pattern
    head_shoulder_mask = df['head_shoulder_pattern'] == 'Head and Shoulder'
    inverse_head_shoulder_mask = df['head_shoulder_pattern'] == 'Inverse Head and Shoulder'

    plt.scatter(df['date'][head_shoulder_mask], df['High'][head_shoulder_mask],
                color='red', label='Head and Shoulder', zorder=5)
    plt.scatter(df['date'][inverse_head_shoulder_mask], df['Low'][inverse_head_shoulder_mask],
                color='green', label='Inverse Head and Shoulder', zorder=5)

    # Add labels, legend, and title
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Head and Shoulder Pattern')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()