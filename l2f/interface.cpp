#include "common.h"


#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
#define L2F_VECTOR
#ifdef L2F_VECTOR
    #ifndef L2F_VECTOR_N_ENVIRONMENTS
        #define L2F_VECTOR_N_ENVIRONMENTS 1024
    #endif
#include "vector.h"
#include <pybind11/numpy.h>
#endif

template <TI N_ENVIRONMENTS>
py::module_ vector_factory(py::module_ &m){
    std::string name = "vector";
    name += std::to_string(N_ENVIRONMENTS);
    py::module_ vector = m.def_submodule(name.c_str());
    vector.def("initialize_environment", &vector::initialize_environment<N_ENVIRONMENTS>, "Init environement");
    vector.def("step", &vector::step<N_ENVIRONMENTS>, "Simulate one step");
    py::class_<vector::Environment<N_ENVIRONMENTS>>(vector, "VectorEnvironment")
        .def(py::init<>())
        .def_property_readonly("OBSERVATION_DIM", [](const vector::Environment<N_ENVIRONMENTS> &self) { return ENVIRONMENT::Observation::DIM; })
        .def_property_readonly("N_ENVIRONMENTS", [](const vector::Environment<N_ENVIRONMENTS> &self) { return vector::Environment<N_ENVIRONMENTS>::N_ENVIRONMENTS; })
        .def_property_readonly("ACTION_DIM", [](const vector::Environment<N_ENVIRONMENTS> &self) { return ENVIRONMENT::ACTION_DIM; })
        .def_readwrite("environments", &vector::Environment<N_ENVIRONMENTS>::environments);
    py::class_<vector::Parameters<N_ENVIRONMENTS>>(vector, "VectorParameters")
        .def(py::init<>())
        .def_readwrite("parameters", &vector::Parameters<N_ENVIRONMENTS>::parameters);
    py::class_<vector::State<N_ENVIRONMENTS>>(vector, "VectorState")
        .def(py::init<>())
        .def("assign", [](vector::State<N_ENVIRONMENTS> &self, const vector::State<N_ENVIRONMENTS> &other) {
            self = other;
        })
        .def("__copy__", [](const vector::State<N_ENVIRONMENTS> &self) {
            return vector::State<N_ENVIRONMENTS>(self);
        })
        .def_readwrite("states", &vector::State<N_ENVIRONMENTS>::states);
    // py::class_<vector::PAD<ENVIRONMENT>, ENVIRONMENT>(vector, "Environment")
    //     .def(py::init<>())
    //     .def(py::init<ENVIRONMENT>());
    // py::class_<vector::PAD<ENVIRONMENT::Parameters>, ENVIRONMENT::Parameters>(vector, "Parameters")
    //     .def(py::init<>())
    //     .def(py::init<ENVIRONMENT::Parameters>());
    // py::class_<vector::PAD<ENVIRONMENT::State>, ENVIRONMENT::State>(vector, "State")
    //     .def(py::init<>())
    //     .def(py::init<ENVIRONMENT::State>())
    //     .def("get_pointer", [](vector::PAD<ENVIRONMENT::State> &self) {
    //         return reinterpret_cast<uintptr_t>(&self);
    //     }, "Get the pointer address of the object");

    vector.def("initial_parameters", &vector::initial_parameters<N_ENVIRONMENTS>, "Reset to default parameters");
    vector.def("sample_initial_parameters", &vector::sample_initial_parameters<N_ENVIRONMENTS>, "Reset to random parameters");
    vector.def("initial_state", &vector::initial_state<N_ENVIRONMENTS>, "Reset to default state");
    vector.def("sample_initial_state", &vector::sample_initial_state<N_ENVIRONMENTS>, "Reset to random state");
    vector.def("step", &vector::step<N_ENVIRONMENTS>, "Simulate one step");
    vector.def("observe", &vector::observe<N_ENVIRONMENTS>, "Observe state");
    return vector;
}


PYBIND11_MODULE(interface, m) {
    py::class_<DEVICE>(m, "Device")
        .def(py::init<>());
    py::class_<RNG>(m, "Rng")
        .def(py::init<>());
    py::class_<ENVIRONMENT>(m, "Environment")
        .def(py::init<>())
        .def_property_readonly("OBSERVATION_DIM", [](const ENVIRONMENT &self) { return ENVIRONMENT::Observation::DIM; });
    py::class_<ENVIRONMENT::Parameters>(m, "Parameters")
        .def(py::init<>())
        .def("__copy__", [](const ENVIRONMENT::Parameters &self) {
            return ENVIRONMENT::Parameters(self);
        })
        .def_readwrite("dynamics", &ENVIRONMENT::Parameters::dynamics)
        .def_readwrite("integration", &ENVIRONMENT::Parameters::integration);
    py::class_<ENVIRONMENT::Parameters::Dynamics>(m, "DynamicsParameters")
        .def(py::init<>())
        .def("__copy__", [](const ENVIRONMENT::Parameters::Dynamics &self) {
            return ENVIRONMENT::Parameters::Dynamics(self);
        })
        .def_property("rotor_positions",
            [](ENVIRONMENT::Parameters::Dynamics &self) -> std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> {
                std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> result;
                for (TI i = 0; i < ENVIRONMENT::Parameters::N; ++i) {
                    std::copy(std::begin(self.rotor_positions[i]), std::end(self.rotor_positions[i]), result[i].begin());
                }
                return result;
            },
            [](ENVIRONMENT::Parameters::Dynamics &self, const std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> &new_data) {
                for (TI i = 0; i < ENVIRONMENT::Parameters::N; ++i) {
                    std::copy(new_data[i].begin(), new_data[i].end(), std::begin(self.rotor_positions[i]));
                }
            }
        )
        .def_property("rotor_thrust_directions",
            [](ENVIRONMENT::Parameters::Dynamics &self) -> std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> {
                std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> result;
                for (TI i = 0; i < ENVIRONMENT::Parameters::N; ++i) {
                    std::copy(std::begin(self.rotor_thrust_directions[i]), std::end(self.rotor_thrust_directions[i]), result[i].begin());
                }
                return result;
            },
            [](ENVIRONMENT::Parameters::Dynamics &self, const std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> &new_data) {
                for (TI i = 0; i < ENVIRONMENT::Parameters::N; ++i) {
                    std::copy(new_data[i].begin(), new_data[i].end(), std::begin(self.rotor_thrust_directions[i]));
                }
            }
        )
        .def_property("rotor_torque_directions",
            [](ENVIRONMENT::Parameters::Dynamics &self) -> std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> {
                std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> result;
                for (TI i = 0; i < ENVIRONMENT::Parameters::N; ++i) {
                    std::copy(std::begin(self.rotor_torque_directions[i]), std::end(self.rotor_torque_directions[i]), result[i].begin());
                }
                return result;
            },
            [](ENVIRONMENT::Parameters::Dynamics &self, const std::array<std::array<T, 3>, ENVIRONMENT::Parameters::N> &new_data) {
                for (TI i = 0; i < ENVIRONMENT::Parameters::N; ++i) {
                    std::copy(new_data[i].begin(), new_data[i].end(), std::begin(self.rotor_torque_directions[i]));
                }
            }
        )
        .def_property("rotor_thrust_coefficients",
            [](ENVIRONMENT::Parameters::Dynamics &self) -> std::array<T, 3> {
                std::array<T, 3> result;
                std::copy(std::begin(self.rotor_thrust_coefficients), std::end(self.rotor_thrust_coefficients), result.begin());
                return result;
            },
            [](ENVIRONMENT::Parameters::Dynamics &self, const std::array<T, 3> &new_data) {
                std::copy(new_data.begin(), new_data.end(), std::begin(self.rotor_thrust_coefficients));
            }
        )
        .def_readwrite("rotor_torque_constant", &ENVIRONMENT::Parameters::Dynamics::rotor_torque_constant)
        .def_readwrite("mass", &ENVIRONMENT::Parameters::Dynamics::mass)
        .def_property("J",
            [](ENVIRONMENT::Parameters::Dynamics &self) -> std::array<std::array<T, 3>, 3> {
                std::array<std::array<T, 3>, 3> result;
                for (TI i = 0; i < 3; ++i) {
                    std::copy(std::begin(self.J[i]), std::end(self.J[i]), result[i].begin());
                }
                return result;
            },
            [](ENVIRONMENT::Parameters::Dynamics &self, const std::array<std::array<T, 3>, 3> &new_data) {
                for (TI i = 0; i < 3; ++i) {
                    std::copy(new_data[i].begin(), new_data[i].end(), std::begin(self.J[i]));
                }
            }
        )
        .def_property("J_inv",
            [](ENVIRONMENT::Parameters::Dynamics &self) -> std::array<std::array<T, 3>, 3> {
                std::array<std::array<T, 3>, 3> result;
                for (TI i = 0; i < 3; ++i) {
                    std::copy(std::begin(self.J_inv[i]), std::end(self.J_inv[i]), result[i].begin());
                }
                return result;
            },
            [](ENVIRONMENT::Parameters::Dynamics &self, const std::array<std::array<T, 3>, 3> &new_data) {
                for (TI i = 0; i < 3; ++i) {
                    std::copy(new_data[i].begin(), new_data[i].end(), std::begin(self.J_inv[i]));
                }
            }
        )
        .def_readwrite("motor_time_constant", &ENVIRONMENT::Parameters::Dynamics::motor_time_constant);
    py::class_<ENVIRONMENT::Parameters::Integration>(m, "IntegrationParameters")
        .def(py::init<>())
        .def_readwrite("dt", &ENVIRONMENT::Parameters::Integration::dt);
    py::class_<ENVIRONMENT::State>(m, "State")
    .def(py::init<>())
    .def("__copy__", [](const ENVIRONMENT::State &self) {
        return ENVIRONMENT::State(self);
    })
    .def("assign", [](ENVIRONMENT::State &self, const ENVIRONMENT::State &other) {
        self = other;
    })
    .def_property("position",
        [](ENVIRONMENT::State &self) -> std::array<T, 3> {
            std::array<T, 3> position;
            std::copy(std::begin(self.position), std::end(self.position), position.begin());
            return position;
        },
        [](ENVIRONMENT::State &self, const std::array<T, 3> &new_data) {
            std::copy(new_data.begin(), new_data.end(), std::begin(self.position));
        }
    )
    .def_property("orientation",
        [](ENVIRONMENT::State &self) -> std::array<T, 4> {
            std::array<T, 4> orientation;
            std::copy(std::begin(self.orientation), std::end(self.orientation), orientation.begin());
            return orientation;
        },
        [](ENVIRONMENT::State &self, const std::array<T, 4> &new_data) {
            std::copy(new_data.begin(), new_data.end(), std::begin(self.orientation));
        }
    )
    .def_property("linear_velocity",
        [](ENVIRONMENT::State &self) -> std::array<T, 3> {
            std::array<T, 3> linear_velocity;
            std::copy(std::begin(self.linear_velocity), std::end(self.linear_velocity), linear_velocity.begin());
            return linear_velocity;
        },
        [](ENVIRONMENT::State &self, const std::array<T, 3> &new_data) {
            std::copy(new_data.begin(), new_data.end(), std::begin(self.linear_velocity));
        }
    )
    .def_property("angular_velocity",
        [](ENVIRONMENT::State &self) -> std::array<T, 3> {
            std::array<T, 3> angular_velocity;
            std::copy(std::begin(self.angular_velocity), std::end(self.angular_velocity), angular_velocity.begin());
            return angular_velocity;
        },
        [](ENVIRONMENT::State &self, const std::array<T, 3> &new_data) {
            std::copy(new_data.begin(), new_data.end(), std::begin(self.angular_velocity));
        }
    )
    .def_property("rpm", 
        [](ENVIRONMENT::State &self) -> std::array<T, 4> {
            std::array<T, 4> rpm;
            std::copy(std::begin(self.rpm), std::end(self.rpm), rpm.begin());
            return rpm;
        },
        [](ENVIRONMENT::State &self, const std::array<T, 4> &new_data) {
            std::copy(new_data.begin(), new_data.end(), std::begin(self.rpm));
        }
    );

    py::class_<Observation>(m, "Observation")
        .def(py::init<>())
        .def_property_readonly("DIM", [](const Observation &self) { return Observation::DIM; })
        .def_readwrite("observation", &Observation::observation);



    m.def("initialize_environment", &initialize_environment, "Init environement");
    m.def("initialize_rng", &initialize_rng, "Init Rng");
    m.def("step", &step, "Simulate one step");
    m.def("initial_parameters", &initial_parameters, "Reset to default parameters");
    m.def("sample_initial_parameters", &sample_initial_parameters, "Reset to random parameters");
    m.def("initial_state", &initial_state, "Reset to default state");
    m.def("sample_initial_state", &sample_initial_state, "Reset to random state");
    m.def("observe", &observe, "Observe state");
    m.def("parameters_to_json", &parameters_to_json, "Convert parameters to json");

#ifdef L2F_VECTOR
    vector_factory<1>(m);
    vector_factory<L2F_VECTOR_N_ENVIRONMENTS>(m);
#endif
}