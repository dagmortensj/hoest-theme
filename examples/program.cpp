// Eksempelfil for å se Høst-temaene på C++.
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

namespace fysikk {

constexpr double G = 6.674e-11;

struct Legeme {
    std::string navn;
    double masse;
    double x = 0.0, y = 0.0;
};

template <typename T>
class Simulering {
public:
    explicit Simulering(double dt) : dt_(dt) {}
    virtual ~Simulering() = default;

    void legg_til(const T& legeme) { legemer_.push_back(legeme); }

    [[nodiscard]] double kraft(const T& a, const T& b) const {
        const auto r = std::hypot(b.x - a.x, b.y - a.y);
        if (r == 0.0) throw std::runtime_error("Kollisjon\n");
        return G * a.masse * b.masse / (r * r);
    }

private:
    std::vector<T> legemer_;
    double dt_;
};

}  // namespace fysikk

int main() {
    using namespace fysikk;
    Simulering<Legeme> sim{0.01};
    auto sola = Legeme{"Sola", 1.989e30};
    for (auto i = 0u; i < 3; ++i) {
        std::cout << "Steg " << i << ": " << sola.navn << '\n';
    }
    return nullptr == nullptr ? 0 : 1;
}
