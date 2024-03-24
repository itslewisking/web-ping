import statistics
import ast

def mean(values: list[str]) -> str:
    total = sum(values) / len(values)
    return f"{total:.3f}"


def mode(values: list[str]) -> str:
    to_compare = [result[:4] for result in values]
    occurences = {}
    for value in to_compare:
        occurences.setdefault(value, 0)
        occurences[value] += 1
    return f"{max(occurences,key=lambda x: occurences[x])}0"


def quotient(values: list[float], q: int) -> str:
    position_raw = (q * (len(values) + 1)) / 4  # q*(n+1)/4
    position = int(position_raw)
    offset = 0
    if position_raw > position:
        offset = (position_raw - position) * (values[position + 1] - values[position])
    return f"{(values[position] + offset):.3f}"


def inter_quartile_range(q3: str, q1: str) -> str:
    return f"{(float(q3) - float(q1)):.3f}"


def median_mean_percentage(median: str, mean: str) -> str:
    return ((float(mean) - float(median)) / float(median)) * 100
    # i.e. how much more the mode is than the median


def build_results(result_sets) -> dict[str, str]:
    combined_results = [value for sublist in result_sets for value in sublist]
    combined_floats = [float(x) for x in combined_results]
    sorted_floats = sorted(combined_floats)
    results = {
        "min_time": f"{min(combined_floats):.3f}",
        "max_time": f"{max(combined_floats):.3f}",
        "range": f"{(max(combined_floats) - min(combined_floats)):.3f}",
        "q1": quotient(sorted_floats, 1),
        "q2": quotient(sorted_floats, 2),
        "q3": quotient(sorted_floats, 3),
        "iqr": inter_quartile_range(
            quotient(sorted_floats, 3), quotient(sorted_floats, 1)
        ),
        "median": f"{statistics.median(combined_floats):.3f}",
        "mean": f"{statistics.mean(combined_floats):.3f}",
        "mode": f"{mode(combined_results)}",
        "median_mean_percentage": f"{median_mean_percentage(str(statistics.median(combined_floats)),str(statistics.mean(combined_floats))):.2f}",
    }
    return results


def load_from_log() -> dict[str, str]:
    with open("last_run.txt", 'r') as f:
        lists = f.readlines()
    list_of_lists = [ast.literal_eval(s.rstrip(',\n')) for s in list(lists)]
    print(build_results(list_of_lists))


if __name__ == "__main__":
    sample_results = [
        ["0.500", "0.281", "0.453", "0.515", "0.453"],
        ["0.360", "0.297", "0.297", "0.328", "0.360"],
        ["0.453", "0.610", "0.625", "0.610", "0.625"],
        ["0.406", "0.344", "0.406", "0.406", "0.344"],
        ["0.375", "0.297", "0.391", "0.407", "0.360"],
        ["0.500", "0.484", "0.391", "0.484", "0.453"],
        ["0.391", "0.328", "0.328", "0.391", "0.375"],
        ["0.406", "0.390", "0.390", "0.406", "0.375"],
        ["0.437", "0.375", "0.406", "0.437", "0.359"],
        ["0.390", "0.375", "0.390", "0.312", "0.359"],
    ]

    print(build_results(sample_results))
