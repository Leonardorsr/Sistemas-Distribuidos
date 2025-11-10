const { createApp } = Vue;

createApp({
    data() {
        return {
            // URL do backend
            apiUrl: 'http://localhost:5000/api',
            
            // Dados
            turmas: [],
            alunos: [],
            turmaSelecionada: '',
            dataAtual: new Date().toISOString().split('T')[0],
            
            // Estados de loading
            loadingTurmas: false,
            loadingAlunos: false,
            salvando: false,
            
            // Toast
            toast: {
                show: false,
                message: '',
                type: 'success'
            }
        }
    },

    computed: {
        totalAlunos() {
            return this.alunos.length;
        },

        totalPresentes() {
            return this.alunos.filter(a => a.presente).length;
        },

        totalAusentes() {
            return this.alunos.filter(a => !a.presente).length;
        }
    },

    methods: {
        /**
         * Carrega lista de turmas do backend
         */
        async carregarTurmas() {
            this.loadingTurmas = true;
            
            try {
                const response = await axios.get(`${this.apiUrl}/turmas`);
                
                if (response.data.success) {
                    this.turmas = response.data.data;
                    console.log('✅ Turmas carregadas:', this.turmas.length);
                } else {
                    throw new Error(response.data.message || 'Erro ao carregar turmas');
                }
            } catch (error) {
                console.error('❌ Erro ao carregar turmas:', error);
                this.mostrarToast('Erro ao carregar turmas. Verifique se o backend está rodando.', 'error');
                
                // Fallback: dados mockados para desenvolvimento
                this.turmas = [
                    { id: 1, nome: '1º Ano A - Matemática (Mock)', quantidade_alunos: 0 },
                    { id: 2, nome: '1º Ano B - Matemática (Mock)', quantidade_alunos: 0 }
                ];
            } finally {
                this.loadingTurmas = false;
            }
        },

        /**
         * Carrega alunos de uma turma específica
         */
        async carregarAlunos() {
            if (!this.turmaSelecionada) {
                this.alunos = [];
                return;
            }

            this.loadingAlunos = true;
            this.alunos = []; // Limpa lista anterior

            try {
                const response = await axios.get(
                    `${this.apiUrl}/turmas/${this.turmaSelecionada}/alunos`
                );
                
                if (response.data.success) {
                    this.alunos = response.data.data;
                    console.log('✅ Alunos carregados:', this.alunos.length);
                    
                    if (this.alunos.length === 0) {
                        this.mostrarToast('Nenhum aluno encontrado nesta turma', 'error');
                    }
                } else {
                    throw new Error(response.data.message || 'Erro ao carregar alunos');
                }
            } catch (error) {
                console.error('❌ Erro ao carregar alunos:', error);
                
                if (error.response && error.response.status === 404) {
                    this.mostrarToast('Turma não encontrada ou sem alunos', 'error');
                } else {
                    this.mostrarToast('Erro ao carregar alunos. Verifique o backend.', 'error');
                }
                
                this.alunos = [];
            } finally {
                this.loadingAlunos = false;
            }
        },

        /**
         * Marca presença ou falta de um aluno
         */
        marcarPresenca(aluno, presente) {
            aluno.presente = presente;
            console.log(`📝 ${aluno.nome}: ${presente ? 'PRESENTE' : 'AUSENTE'}`);
        },

        /**
         * Salva presenças no backend
         */
        async salvarPresencas() {
            if (!this.turmaSelecionada) {
                this.mostrarToast('Selecione uma turma primeiro', 'error');
                return;
            }

            if (this.alunos.length === 0) {
                this.mostrarToast('Nenhum aluno para salvar', 'error');
                return;
            }

            this.salvando = true;

            try {
                const dados = {
                    turma_id: parseInt(this.turmaSelecionada),
                    data: this.dataAtual,
                    presencas: this.alunos.map(aluno => ({
                        aluno_id: aluno.id,  // Mantém como string (ex: "2024001")
                        presente: aluno.presente
                    }))
                };

                console.log('💾 Salvando presenças:', dados);
                
                const response = await axios.post(
                    `${this.apiUrl}/presencas`,
                    dados,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                );
                
                if (response.data.success) {
                    this.mostrarToast('✓ Presenças salvas com sucesso!', 'success');
                    console.log('✅ Resposta do servidor:', response.data.message);
                    
                    // Recarregar alunos para pegar status atualizado do CSV
                    await this.carregarAlunos();
                } else {
                    throw new Error(response.data.message || 'Erro ao salvar');
                }
            } catch (error) {
                console.error('❌ Erro ao salvar presenças:', error);
                
                if (error.response) {
                    // Erro retornado pelo servidor
                    const message = error.response.data.message || 'Erro no servidor';
                    this.mostrarToast(`✗ ${message}`, 'error');
                } else if (error.request) {
                    // Requisição feita mas sem resposta
                    this.mostrarToast('✗ Sem resposta do servidor. Backend está rodando?', 'error');
                } else {
                    // Erro ao configurar requisição
                    this.mostrarToast('✗ Erro ao enviar dados', 'error');
                }
            } finally {
                this.salvando = false;
            }
        },

        /**
         * Exibe mensagem toast
         */
        mostrarToast(message, type = 'success') {
            this.toast.message = message;
            this.toast.type = type;
            this.toast.show = true;

            setTimeout(() => {
                this.toast.show = false;
            }, 3000);
        },

        /**
         * Marcar todos como presente
         */
        marcarTodosPresente() {
            this.alunos.forEach(aluno => {
                aluno.presente = true;
            });
            this.mostrarToast('Todos marcados como presentes', 'success');
        },

        /**
         * Marcar todos como ausente
         */
        marcarTodosAusente() {
            this.alunos.forEach(aluno => {
                aluno.presente = false;
            });
            this.mostrarToast('Todos marcados como ausentes', 'error');
        }
    },

    /**
     * Inicialização quando o componente é montado
     */
    mounted() {
        console.log('🚀 Sistema de Presença iniciado');
        console.log('🔗 Backend URL:', this.apiUrl);
        this.carregarTurmas();
    }
}).mount('#app');
